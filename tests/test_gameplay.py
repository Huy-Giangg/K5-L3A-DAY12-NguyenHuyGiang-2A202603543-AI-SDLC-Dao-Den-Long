import pytest
from src.core.models import Tuning, PlayerState, LanternState, ShadeState, MoteState
from src.core.engine import SimulationEngine

def test_mote_pickup_and_capacity():
    tuning = Tuning(carry_capacity=2, pickup_radius=1.5)
    engine = SimulationEngine(tuning=tuning)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.motes = [
        MoteState(id="M1", pos=[0.0, 0.0, 1.0]),
        MoteState(id="M2", pos=[0.0, 0.0, 1.2]),
        MoteState(id="M3", pos=[0.0, 0.0, 1.4]),
    ]
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    # Should pick up 2 motes max
    assert engine.player.carried == 2
    assert sum(1 for m in engine.motes if m.active) == 1
    picked_events = [e for e in engine.events_this_tick if e["name"] == "mote_picked"]
    assert len(picked_events) == 2

def test_deposit_and_lantern_lit():
    tuning = Tuning(lantern_cost=3, interact_radius=2.0)
    engine = SimulationEngine(tuning=tuning)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 3
    engine.lanterns = [
        LanternState(id="L1", pos=[0.0, 0.0, 1.5], deposited=1, lit=False)
    ]
    engine.random_motes = False
    engine.random_shades = False

    engine.current_interact = True
    engine.step()

    assert engine.lanterns[0].deposited == 3
    assert engine.lanterns[0].lit is True
    assert engine.player.carried == 1 # 2 deposited

    events = [e["name"] for e in engine.events_this_tick]
    assert "deposit" in events
    assert "lantern_lit" in events

def test_pulse_stuns_and_pushes_shades():
    tuning = Tuning(pulse_cost=1, pulse_radius=5.0, pulse_push_m=3.0, pulse_stun_s=3.0)
    engine = SimulationEngine(tuning=tuning)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 2
    engine.shades = [
        ShadeState(id="S1", pos=[0.0, 0.0, 2.0], state="chase"),
        ShadeState(id="S2", pos=[0.0, 0.0, 10.0], state="chase") # outside pulse radius
    ]
    engine.random_motes = False
    engine.random_shades = False

    engine.current_pulse = True
    engine.step()

    assert engine.player.carried == 1
    assert engine.shades[0].state == "stunned"
    assert engine.shades[0].stun_timer > 0

    pulse_event = next(e for e in engine.events_this_tick if e["name"] == "pulse")
    assert "S1" in pulse_event["data"]["stunned_ids"]
    assert "S2" not in pulse_event["data"]["stunned_ids"]

    # Ticket-02 spec: pulse push is distributed over 15 ticks instead of instant.
    # After 1 step, push has started:
    assert engine.shades[0].pos[2] > 2.0
    # Simulate remaining 14 ticks of push:
    for _ in range(14):
        engine.step()
    assert engine.shades[0].pos[2] >= 4.9 # Total push completes over 15 ticks
    assert engine.shades[1].state == "chase" # unaffected

def test_player_hit_and_invulnerability():
    tuning = Tuning(invuln_s=2.0, hit_drop_ratio=0.5, shade_hit_radius=1.0)
    engine = SimulationEngine(tuning=tuning)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.player.carried = 4
    engine.player.flames = 3
    engine.shades = [ShadeState(id="S1", pos=[0.0, 0.0, 0.5], state="chase")]
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    assert engine.player.flames == 2
    assert engine.player.carried == 2 # dropped 2 motes
    assert engine.player.invuln_timer > 0

    hit_event = next(e for e in engine.events_this_tick if e["name"] == "player_hit")
    assert hit_event["data"]["flames"] == 2
    assert hit_event["data"]["dropped"] == 2

    # Next step during invulnerability should not hit again
    engine.step()
    assert engine.player.flames == 2

def test_safe_zone_repels_shades():
    tuning = Tuning(safe_radius=5.0)
    engine = SimulationEngine(tuning=tuning)
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.lanterns = [LanternState(id="L1", pos=[0.0, 0.0, 10.0], lit=True)]
    engine.shades = [ShadeState(id="S1", pos=[0.0, 0.0, 11.0], state="chase")]
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    dist_to_lantern = abs(engine.shades[0].pos[2] - 10.0)
    assert dist_to_lantern > 5.0 # Repelled outside safe radius

def test_game_over_win():
    engine = SimulationEngine()
    engine.player.pos = [0.0, 0.0, 0.0]
    engine.lanterns = [
        LanternState(id=f"L{i}", pos=[0.0, 0.0, float(i*5)], lit=True, deposited=5)
        for i in range(1, 6)
    ]
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    assert engine.state == "won"
    assert any(e["name"] == "game_over" and e["data"]["result"] == "won" and e["data"]["reason"] == "all_lit" for e in engine.events_this_tick)

def test_game_over_lost_no_flames():
    engine = SimulationEngine()
    engine.player.flames = 0
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    assert engine.state == "lost"
    assert any(e["name"] == "game_over" and e["data"]["result"] == "lost" and e["data"]["reason"] == "no_flames" for e in engine.events_this_tick)

def test_game_over_lost_dawn():
    engine = SimulationEngine()
    engine.time_left_s = 0.001
    engine.random_motes = False
    engine.random_shades = False

    engine.step()
    assert engine.state == "lost"
    assert any(e["name"] == "game_over" and e["data"]["result"] == "lost" and e["data"]["reason"] == "dawn" for e in engine.events_this_tick)

