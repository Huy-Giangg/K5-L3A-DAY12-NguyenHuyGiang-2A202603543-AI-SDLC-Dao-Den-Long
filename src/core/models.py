from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Tuning:
    player_speed: float = 5.0
    carry_capacity: int = 10
    lantern_cost: int = 5
    lantern_count_night1: int = 5
    pickup_radius: float = 1.5
    interact_radius: float = 2.5
    pulse_cost: int = 1
    pulse_radius: float = 6.0
    night1_duration_s: float = 300.0
    flames: int = 3
    invuln_s: float = 2.0
    hit_drop_ratio: float = 0.5
    pulse_stun_s: float = 3.0
    pulse_push_m: float = 3.0
    pulse_cooldown_s: float = 1.0
    safe_radius: float = 5.0
    shade_speed: float = 3.2
    shade_hit_radius: float = 1.0
    fall_enabled: bool = False
    per_mote_score: int = 10
    per_lantern_score: int = 200
    per_stun_score: int = 25
    per_second_left_score: int = 5
    per_flame_left_score: int = 100

@dataclass
class PlayerState:
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    carried: int = 0
    flames: int = 3
    invuln_timer: float = 0.0
    pulse_cooldown: float = 0.0

@dataclass
class LanternState:
    id: str
    pos: List[float]
    lit: bool = False
    deposited: int = 0

@dataclass
class ShadeState:
    id: str
    pos: List[float]
    state: str = "chase"
    stun_timer: float = 0.0

@dataclass
class MoteState:
    id: str
    pos: List[float]
    active: bool = True

