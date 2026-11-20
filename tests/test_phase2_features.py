import json
import os
import subprocess
import sys
import time
import pytest
from src.core.models import Tuning, LanternState, ShadeState, MoteState, DrifterState, CharmState
from src.core.engine import SimulationEngine

def test_dash_mechanic():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.facing_dir = [0.0, 0.0, 1.0]

    # Trigger dash while standing still
    engine.current_dash = True
    engine.step()

    assert engine.player.dash_ticks_left == 11 # 1 tick consumed
    assert engine.player.dash_cd_ticks > 0
    dash_events = [e for e in engine.events_this_tick if e["name"] == "dash"]
    assert len(dash_events) == 1

    # Distance after 1 tick: 14 m/s * (1/60) = 0.2333m
    assert pytest.approx(engine.player.pos[2], abs=0.01) == 0.233

def test_jump_mechanic():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.grounded = True

    engine.current_jump = True
    engine.step()

    assert not engine.player.grounded
    # Initial vy = 7.0 - 20 * (1/60) = 6.667 m/s
    assert engine.player.pos[1] > 0.0

def test_charm_buff_and_infinite_dash():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=2)
    engine.player.pos = [35.0, 0.0, 0.0] # Near charm C1 at (35,0,0)
    engine.charms = [CharmState(id="C1", pos=[35.0, 0.0, 0.0], available=True)]

    engine.step()
    # Should pick charm
    picked_event = next(e for e in engine.events_this_tick if e["name"] == "charm_picked")
    assert picked_event["data"]["charm_id"] == "C1"
    assert engine.player.charm_ticks_left == 600
    assert not engine.charms[0].available
    assert engine.charms[0].respawn_ticks == 2700

def test_drifter_steal_and_pulse_drop():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=2)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 6 # >= 5 motes to trigger drifter chase
    engine.drifters = [DrifterState(id="D1", pos=[0.0, 0.0, 1.0], state="chase")]

    engine.step()
    # Drifter should steal min(3, carried) = 3 motes
    steal_event = next(e for e in engine.events_this_tick if e["name"] == "drifter_steal")
    assert steal_event["data"]["drifter_id"] == "D1"
    assert steal_event["data"]["amount"] == 3
    assert engine.player.carried == 3
    assert engine.drifters[0].stolen == 3
    assert engine.drifters[0].state == "flee"

    # Now player pulses: drifter is in flee state with stolen goods -> should drop motes
    engine.current_pulse = True
    engine.step()
    drop_events = [e for e in engine.events_this_tick if e["name"] == "drifter_drop"]
    assert len(drop_events) == 1
    assert drop_events[0]["data"]["drifter_id"] == "D1"
    assert drop_events[0]["data"]["amount"] == 3
    assert engine.drifters[0].stolen == 0

def test_jumppad_launch():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=2)
    # Move player onto jump pad at (20, 0, 18)
    engine.player.pos = [20.0, 0.0, 18.0]
    engine.player.grounded = True

    engine.step()
    assert engine.player.jumppad_flight is True
    assert engine.player.vel[1] > 0.0
    assert engine.player.vel[0] > 0.0 # launching towards Island B (center 70, 0, 0)

def test_fall_off_island():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [50.0, -11.0, 0.0] # Y < -10, in void
    engine.player.carried = 5
    engine.player.flames = 3

    engine.step()
    hit_events = [e for e in engine.events_this_tick if e["name"] == "player_hit"]
    assert len(hit_events) == 1
    assert hit_events[0]["data"]["by"] == "fall"
    assert hit_events[0]["data"]["flames"] == 2
    assert hit_events[0]["data"]["lost"] == 5
    assert engine.player.carried == 0
    assert engine.player.fall_wait_ticks == 60

def test_pause_and_resume():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.time_left_s = 300.0

    # Trigger pause
    engine.current_pause = True
    engine.step()

    assert engine.state == "paused"
    paused_events = [e for e in engine.events_this_tick if e["name"] == "paused"]
    assert len(paused_events) == 1

    # While paused, time and sim_tick do not decrease
    time_before = engine.time_left_s
    sim_before = engine.sim_tick
    engine.current_pause = False
    engine.step()
    assert engine.time_left_s == time_before
    assert engine.sim_tick == sim_before
    assert engine.state == "paused"

    # Trigger unpause
    engine.current_pause = True
    engine.step()
    assert engine.state == "playing"
    resumed_events = [e for e in engine.events_this_tick if e["name"] == "resumed"]
    assert len(resumed_events) == 1

def test_night2_and_night3_setup():
    e2 = SimulationEngine(night=2)
    assert len(e2.lanterns) == 6
    assert len(e2.jump_pads) == 2
    assert len(e2.charms) == 1

    e3 = SimulationEngine(night=3)
    assert len(e3.lanterns) == 7
    assert len(e3.jump_pads) == 1
    assert len(e3.charms) == 2
    assert e3.wind_enabled is True

def test_headless_full_night_performance(tmp_path):
    out_file = str(tmp_path / "perf.jsonl")
    cmd = [
        sys.executable, "-m", "src.main", "--headless",
        "--seed", "42",
        "--night", "1",
        "--ticks", "21600",
        "--out", out_file,
        "--snapshot-every", "600"
    ]
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - t0

    assert res.returncode == 0, f"Error: {res.stderr}"
    assert duration <= 30.0, f"Full night simulation must complete within 30s, took {duration:.2f}s"
    print(f"Performance: 21,600 ticks simulated in {duration:.2f} seconds!")

