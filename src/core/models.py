from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Tuning:
    player_speed: float = 6.0
    carry_capacity: int = 10
    lantern_cost: int = 10
    lantern_count_night1: int = 5
    pickup_radius: float = 1.0
    interact_radius: float = 2.0
    pulse_cost: int = 3
    pulse_radius: float = 5.0
    pulse_cooldown_s: float = 3.0
    pulse_stun_s: float = 2.0
    pulse_push_m: float = 4.0
    night1_duration_s: float = 300.0
    night2_duration_s: float = 330.0
    night3_duration_s: float = 360.0
    flames: int = 3
    invuln_s: float = 1.5
    hit_drop_ratio: float = 0.5
    safe_radius: float = 6.0
    shade_speed: float = 4.0
    shade_hit_radius: float = 1.0
    fall_enabled: bool = True
    dash_speed: float = 14.0
    dash_duration_s: float = 0.2
    dash_cooldown_s: float = 1.5
    per_mote_score: int = 10
    per_lantern_score: int = 100
    per_stun_score: int = 5
    per_second_left_score: int = 2
    per_flame_left_score: int = 50

@dataclass
class PlayerState:
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    vel: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    grounded: bool = True
    invuln: bool = False
    flames: int = 3
    carried: int = 0
    dash_cd_s: float = 0.0
    pulse_cd_s: float = 0.0
    charm_s: float = 0.0

    # Internal tick timers
    invuln_ticks: int = 0
    dash_ticks_left: int = 0
    dash_cd_ticks: int = 0
    pulse_cd_ticks: int = 0
    charm_ticks_left: int = 0
    fall_wait_ticks: int = 0
    facing_dir: List[float] = field(default_factory=lambda: [0.0, 0.0, 1.0])
    dash_dir: List[float] = field(default_factory=lambda: [0.0, 0.0, 1.0])
    jumppad_flight: bool = False

    @property
    def invuln_timer(self) -> float:
        return self.invuln_ticks / 60.0

    @invuln_timer.setter
    def invuln_timer(self, val: float):
        self.invuln_ticks = int(round(val * 60.0))
        self.invuln = self.invuln_ticks > 0

    @property
    def pulse_cooldown(self) -> float:
        return self.pulse_cd_ticks / 60.0

    @pulse_cooldown.setter
    def pulse_cooldown(self, val: float):
        self.pulse_cd_ticks = int(round(val * 60.0))

@dataclass
class LanternState:
    id: str
    pos: List[float]
    lit: bool = False
    deposited: int = 0
    recently_lit_ticks: int = 0

@dataclass
class ShadeState:
    id: str
    pos: List[float]
    state: str = "wander" # spawning, wander, chase, recoil, stunned
    state_ticks_left: int = 0
    recoil_dir: List[float] = field(default_factory=lambda: [0.0, 0.0])
    push_dir: List[float] = field(default_factory=lambda: [1.0, 0.0])
    push_ticks_left: int = 0

    @property
    def stun_timer(self) -> float:
        return self.state_ticks_left / 60.0

    @stun_timer.setter
    def stun_timer(self, val: float):
        self.state_ticks_left = int(round(val * 60.0))
        if self.state_ticks_left > 0:
            self.state = "stunned"

@dataclass
class MoteState:
    id: str
    pos: List[float]
    active: bool = True
    kind: str = "random" # "random" or "dropped"
    ttl_ticks: Optional[int] = None
    age_ticks: int = 0

@dataclass
class DrifterState:
    id: str
    pos: List[float]
    state: str = "idle" # idle, chase, flee, removed
    stolen: int = 0
    state_ticks_left: int = 0
    flee_dir: List[float] = field(default_factory=lambda: [1.0, 0.0, 0.0])
    has_stolen_once: bool = False

@dataclass
class CharmState:
    id: str
    pos: List[float]
    available: bool = True
    respawn_ticks: int = 0

@dataclass
class WindState:
    active: bool = False
    dir_deg: float = 0.0
    cycle_ticks: int = 0
    duration_ticks: int = 0
    wind_vector: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

@dataclass
class JumpPad:
    pos: List[float]
    radius: float = 1.0
    launch_vy: float = 14.0
    launch_hspeed: float = 24.0
    target_dir: Optional[List[float]] = None
