from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Tuning:
    player_speed: float = 6.0
    carry_capacity: int = 10
    capacity_max: int = 20
    lantern_cost: int = 10
    relight_cost: int = 5
    lantern_count_night1: int = 5
    pickup_radius: float = 1.0
    interact_radius: float = 2.0
    pulse_cost: int = 3
    pulse_radius: float = 5.0
    pulse_cooldown_s: float = 3.0
    pulse_stun_s: float = 2.0
    pulse_push_m: float = 4.0
    night1_duration_s: float = 240.0
    night2_duration_s: float = 270.0
    night3_duration_s: float = 300.0
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
    fuel_max: float = 100.0
    fuel_decay_per_s: float = 1.0
    fuel_per_mote: float = 10.0
    drain_per_s: float = 5.0
    low_fuel_threshold: float = 30.0
    win_ratio: float = 0.6
    per_mote_score: int = 5
    per_lantern_score: int = 100
    per_relight_score: int = 40
    per_stun_score: int = 5
    per_stun_drain_score: int = 15
    per_second_left_score: int = 0
    per_flame_left_score: int = 50

@dataclass
class PlayerState:
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    vel: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    grounded: bool = True
    invuln: bool = False
    flames: int = 3
    carried: int = 0
    successful_lights: int = 0
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
    def capacity(self) -> int:
        return min(20, 10 + 2 * self.successful_lights)

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
    fuel: float = 0.0
    ever_lit: bool = False
    relit_count: int = 0
    recently_lit_ticks: int = 0

    def __post_init__(self):
        if self.lit:
            self.ever_lit = True
            if self.fuel <= 0.0:
                self.fuel = 100.0

@dataclass
class ShadeState:
    id: str
    pos: List[float]
    state: str = "wander"
    state_ticks_left: int = 0
    recoil_dir: List[float] = field(default_factory=lambda: [0.0, 0.0])
    push_dir: List[float] = field(default_factory=lambda: [1.0, 0.0])
    push_ticks_left: int = 0
    target_lantern_id: Optional[str] = None
    drain_ticks: int = 0

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
    kind: str = "random"
    ttl_ticks: Optional[int] = None
    age_ticks: int = 0

@dataclass
class DrifterState:
    id: str
    pos: List[float]
    state: str = "idle"
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
