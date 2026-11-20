import json
import math
import pytest
from src.core.models import Tuning, LanternState, ShadeState, MoteState
from src.core.engine import SimulationEngine

def test_fuel_decay_and_lantern_out():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 10.0], lit=True, fuel=0.05)] # fuel will deplete in few ticks
    engine.random_motes = False
    engine.random_shades = False

    engine.step() # 1 tick drops fuel by 1/60 ~ 0.0167 -> remaining ~0.033
    engine.step()
    engine.step() # drops below 0 -> lantern_out

    assert engine.lanterns[0].lit is False
    assert engine.lanterns[0].fuel == 0.0
    assert engine.lanterns[0].ever_lit is True
    out_events = [e for e in engine.events_this_tick if e["name"] == "lantern_out"]
    assert len(out_events) == 1
    assert out_events[0]["data"]["lantern_id"] == "L1"

def test_refuel_mechanic():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 5
    # Lantern L1 is lit but fuel is 75 (needs ceil((100-75)/10) = 3 motes)
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 1.0], lit=True, fuel=75.0)]
    engine.random_motes = False
    engine.random_shades = False

    engine.current_interact = True
    engine.step()

    refuel_events = [e for e in engine.events_this_tick if e["name"] == "refuel"]
    assert len(refuel_events) == 1
    assert refuel_events[0]["data"]["amount"] == 3
    assert engine.player.carried == 2
    assert engine.lanterns[0].fuel >= 100.0 - 0.05 # 75 + 30 = 105 -> clamped to 100
    assert engine.score == 3 * 5 # +5 per mote refueled

def test_relight_cost_discount():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 5
    # Lantern L1 was previously lit (ever_lit = True)
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 1.0], lit=False, deposited=0, ever_lit=True)]
    engine.random_motes = False
    engine.random_shades = False

    engine.current_interact = True
    engine.step()

    assert engine.lanterns[0].lit is True
    assert engine.lanterns[0].relit_count == 1
    assert engine.player.carried == 0 # used 5 motes
    lit_events = [e for e in engine.events_this_tick if e["name"] == "lantern_lit"]
    assert len(lit_events) == 1
    assert lit_events[0]["data"]["relight"] is True
    assert engine.score == 5 * 5 + 40 # 25 (motes) + 40 (relight)

def test_shade_drain_fuel():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 25.0] # far away from shade & lantern
    # Lantern with low fuel (< 30) loses safe zone
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 0.0], lit=True, fuel=25.0)]
    # Shade right at lantern <= 2.0m in wander state
    engine.shades = [ShadeState(id="S1", pos=[0.0, 0.0, 1.0], state="wander")]
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    # Shade should seek weak lantern and transition to drain
    assert engine.shades[0].state == "drain"
    assert engine.shades[0].target_lantern_id == "L1"

    # Advance 60 ticks while draining to trigger fuel_drain event
    for _ in range(60):
        engine.step()

    drain_events = [e for e in engine.events_this_tick if e["name"] == "fuel_drain"]
    assert len(drain_events) == 1
    assert drain_events[0]["data"]["shade_id"] == "S1"

def test_pulse_on_draining_shade():
    tuning = Tuning()
    engine = SimulationEngine(tuning=tuning, night=1)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 3
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 2.0], lit=True, fuel=25.0)]
    engine.shades = [ShadeState(id="S1", pos=[0.0, 0.0, 1.5], state="drain", target_lantern_id="L1")]
    engine.random_motes = False
    engine.random_shades = False

    engine.current_pulse = True
    engine.step()

    assert engine.shades[0].state == "stunned"
    # Draining shade gives +15 score instead of +5
    assert engine.score == 15

def test_capacity_scaling():
    engine = SimulationEngine()
    assert engine.player.capacity == 10
    engine.player.successful_lights = 2
    assert engine.player.capacity == 14
    engine.player.successful_lights = 6
    assert engine.player.capacity == 20 # max 20

def test_dawn_survival_win_and_lose():
    # Test 1: Win when >= 60% lit (3/5 in Night 1)
    e_win = SimulationEngine(night=1)
    e_win.lanterns = [
        LanternState(id="L1", pos=[0,0,0], lit=True, fuel=80.0),
        LanternState(id="L2", pos=[0,0,5], lit=True, fuel=70.0),
        LanternState(id="L3", pos=[0,0,10], lit=True, fuel=60.0),
        LanternState(id="L4", pos=[0,0,15], lit=False, fuel=0.0),
        LanternState(id="L5", pos=[0,0,20], lit=False, fuel=0.0)
    ]
    e_win.time_left_s = 0.0
    e_win.step()
    assert e_win.state == "won"
    assert any(e["name"] == "game_over" and e["data"]["reason"] == "dawn_survived" for e in e_win.events_this_tick)

    # Test 2: Lose when < 60% lit (2/5 in Night 1)
    e_lose = SimulationEngine(night=1)
    e_lose.lanterns = [
        LanternState(id="L1", pos=[0,0,0], lit=True, fuel=80.0),
        LanternState(id="L2", pos=[0,0,5], lit=True, fuel=70.0),
        LanternState(id="L3", pos=[0,0,10], lit=False, fuel=0.0),
        LanternState(id="L4", pos=[0,0,15], lit=False, fuel=0.0),
        LanternState(id="L5", pos=[0,0,20], lit=False, fuel=0.0)
    ]
    e_lose.time_left_s = 0.0
    e_lose.step()
    assert e_lose.state == "lost"
    assert any(e["name"] == "game_over" and e["data"]["reason"] == "dawn" for e in e_lose.events_this_tick)
