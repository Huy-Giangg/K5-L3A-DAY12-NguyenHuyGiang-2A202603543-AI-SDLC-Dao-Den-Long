import math
import random
from typing import List, Dict, Any, Optional, Tuple
from src.core.models import (
    Tuning, PlayerState, LanternState, ShadeState, MoteState,
    DrifterState, CharmState, WindState, JumpPad
)

class SimulationEngine:
    def __init__(self, seed: int = 42, tuning: Optional[Tuning] = None, night: int = 1):
        self.seed = seed
        self.rng = random.Random(seed)
        self.tuning = tuning or Tuning()
        self.night = night
        self.dt = 1.0 / 60.0 # 60 ticks per second

        self.tick = 0
        self.sim_tick = 0
        self.state = "playing" # "playing", "paused", "won", "lost"
        self.prev_state_before_pause = "playing"
        self.score = 0

        # Duration based on night
        if self.night == 1:
            self.total_duration_s = float(self.tuning.night1_duration_s)
        elif self.night == 2:
            self.total_duration_s = float(self.tuning.night2_duration_s)
        else:
            self.total_duration_s = float(self.tuning.night3_duration_s)
        self.time_left_s = self.total_duration_s

        self.player = PlayerState(flames=self.tuning.flames)
        self.lanterns: List[LanternState] = []
        self.shades: List[ShadeState] = []
        self.motes: List[MoteState] = []
        self.drifters: List[DrifterState] = []
        self.charms: List[CharmState] = []
        self.jump_pads: List[JumpPad] = []
        self.wind = WindState()

        self.random_motes = True
        self.random_shades = True
        self.random_drifters = True
        self.wind_enabled = (self.night == 3)

        self.next_shade_id_idx = 1
        self.next_mote_id_idx = 1
        self.next_drifter_id_idx = 1

        self.events_this_tick: List[Dict[str, Any]] = []

        # Previous frame button states for edge detection (false -> true)
        self.prev_interact = False
        self.prev_pulse = False
        self.prev_jump = False
        self.prev_dash = False
        self.prev_pause = False

        # Current control state
        self.current_move = [0.0, 0.0]
        self.current_cam_yaw_deg = 0.0
        self.current_interact = False
        self.current_pulse = False
        self.current_jump = False
        self.current_dash = False
        self.current_pause = False

        # Spawn points for current night
        self.mote_spawn_points: List[List[float]] = []
        self.shade_spawn_points: List[List[float]] = []

        self._init_world_by_night()

    def _init_world_by_night(self):
        self.player.pos = [0.0, 0.0, 0.0]
        self.player.facing_dir = [0.0, 0.0, 1.0]

        if self.night == 1:
            # 5 Lanterns
            self.lanterns = [
                LanternState(id="L1", pos=[0.0, 0.0, 25.0]),
                LanternState(id="L2", pos=[23.8, 0.0, 7.7]),
                LanternState(id="L3", pos=[14.7, 0.0, -20.2]),
                LanternState(id="L4", pos=[-14.7, 0.0, -20.2]),
                LanternState(id="L5", pos=[-23.8, 0.0, 7.7])
            ]
            # Mote spawn points: 8 points R=12 (every 45 deg) + 16 points R=33 (every 22.5 deg)
            for i in range(8):
                deg = i * 45.0
                rad = math.radians(deg)
                self.mote_spawn_points.append([round(12.0 * math.cos(rad), 3), 0.0, round(12.0 * math.sin(rad), 3)])
            for i in range(16):
                deg = i * 22.5
                rad = math.radians(deg)
                self.mote_spawn_points.append([round(33.0 * math.cos(rad), 3), 0.0, round(33.0 * math.sin(rad), 3)])

            # Initial 20 motes placed on first 20 points
            for i in range(min(20, len(self.mote_spawn_points))):
                pt = self.mote_spawn_points[i]
                self.motes.append(MoteState(id=f"M{i+1}", pos=[pt[0], pt[1], pt[2]], kind="random"))
            self.next_mote_id_idx = len(self.motes) + 1

            # Shade spawn points: 12 points R=37 (15, 45, ...)
            for i in range(12):
                deg = 15.0 + i * 30.0
                rad = math.radians(deg)
                self.shade_spawn_points.append([round(37.0 * math.cos(rad), 3), 0.0, round(37.0 * math.sin(rad), 3)])

        elif self.night == 2:
            # 6 Lanterns: (0,0,20), (17,0,-10), (-17,0,-10), (70,0,20), (87,0,-10), (53,0,-10)
            self.lanterns = [
                LanternState(id="L1", pos=[0.0, 0.0, 20.0]),
                LanternState(id="L2", pos=[17.0, 0.0, -10.0]),
                LanternState(id="L3", pos=[-17.0, 0.0, -10.0]),
                LanternState(id="L4", pos=[70.0, 0.0, 20.0]),
                LanternState(id="L5", pos=[87.0, 0.0, -10.0]),
                LanternState(id="L6", pos=[53.0, 0.0, -10.0])
            ]
            # Jump pads: at (20,0,18) targeting B(70,0,0) and (50,0,-18) targeting A(0,0,0)
            dir_a_to_b = [70.0 - 20.0, 0.0, 0.0 - 18.0]
            mag_ab = math.hypot(dir_a_to_b[0], dir_a_to_b[2])
            dir_b_to_a = [0.0 - 50.0, 0.0, 0.0 - (-18.0)]
            mag_ba = math.hypot(dir_b_to_a[0], dir_b_to_a[2])

            self.jump_pads = [
                JumpPad(pos=[20.0, 0.0, 18.0], launch_vy=14.0, launch_hspeed=24.0,
                        target_dir=[dir_a_to_b[0]/mag_ab, 0.0, dir_a_to_b[2]/mag_ab]),
                JumpPad(pos=[50.0, 0.0, -18.0], launch_vy=14.0, launch_hspeed=24.0,
                        target_dir=[dir_b_to_a[0]/mag_ba, 0.0, dir_b_to_a[2]/mag_ba])
            ]

            # Charm C1 at (35,0,0)
            self.charms = [CharmState(id="C1", pos=[35.0, 0.0, 0.0])]

            # Mote spawn points: Island A and Island B
            for center_x in [0.0, 70.0]:
                for deg in [0.0, 90.0, 180.0, 270.0]:
                    rad = math.radians(deg)
                    self.mote_spawn_points.append([round(center_x + 10.0 * math.cos(rad), 3), 0.0, round(10.0 * math.sin(rad), 3)])
                for i in range(8):
                    deg = i * 45.0
                    rad = math.radians(deg)
                    self.mote_spawn_points.append([round(center_x + 22.0 * math.cos(rad), 3), 0.0, round(22.0 * math.sin(rad), 3)])

            # Initial 20 motes
            for i in range(min(20, len(self.mote_spawn_points))):
                pt = self.mote_spawn_points[i]
                self.motes.append(MoteState(id=f"M{i+1}", pos=[pt[0], pt[1], pt[2]], kind="random"))
            self.next_mote_id_idx = len(self.motes) + 1

            # Shade spawn points: 8 points R=26 per island
            for center_x in [0.0, 70.0]:
                for i in range(8):
                    deg = 22.5 + i * 45.0
                    rad = math.radians(deg)
                    self.shade_spawn_points.append([round(center_x + 26.0 * math.cos(rad), 3), 0.0, round(26.0 * math.sin(rad), 3)])

        elif self.night == 3:
            # 7 Lanterns
            self.lanterns = [
                LanternState(id="L1", pos=[0.0, 6.0, 6.0]),
                LanternState(id="L2", pos=[18.0, 3.0, 10.0]),
                LanternState(id="L3", pos=[-18.0, 3.0, 10.0]),
                LanternState(id="L4", pos=[35.0, 0.0, -10.0]),
                LanternState(id="L5", pos=[-35.0, 0.0, -10.0]),
                LanternState(id="L6", pos=[20.0, 0.0, -35.0]),
                LanternState(id="L7", pos=[-20.0, 0.0, -35.0])
            ]
            # Jump pad at (0,3,13) targeting -Z onto tier 2 (Y=6)
            self.jump_pads = [
                JumpPad(pos=[0.0, 3.0, 13.0], launch_vy=12.0, launch_hspeed=8.0, target_dir=[0.0, 0.0, -1.0])
            ]
            # Charms C1 at (30,0,25) and C2 at (-30,0,25)
            self.charms = [
                CharmState(id="C1", pos=[30.0, 0.0, 25.0]),
                CharmState(id="C2", pos=[-30.0, 0.0, 25.0])
            ]
            # Mote spawn points (30): Tier 0 (18 pts R=34), Tier 1 (8 pts R=18), Tier 2 (4 pts R=5)
            for i in range(18):
                deg = i * 20.0
                rad = math.radians(deg)
                self.mote_spawn_points.append([round(34.0 * math.cos(rad), 3), 0.0, round(34.0 * math.sin(rad), 3)])
            for deg in [20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0]:
                rad = math.radians(deg)
                self.mote_spawn_points.append([round(18.0 * math.cos(rad), 3), 3.0, round(18.0 * math.sin(rad), 3)])
            for deg in [45.0, 135.0, 225.0, 315.0]:
                rad = math.radians(deg)
                self.mote_spawn_points.append([round(5.0 * math.cos(rad), 3), 6.0, round(5.0 * math.sin(rad), 3)])

            # Initial 20 motes
            for i in range(min(20, len(self.mote_spawn_points))):
                pt = self.mote_spawn_points[i]
                self.motes.append(MoteState(id=f"M{i+1}", pos=[pt[0], pt[1], pt[2]], kind="random"))
            self.next_mote_id_idx = len(self.motes) + 1

            # Shade spawn points: 16 points R=43 (every 22.5 deg)
            for i in range(16):
                deg = i * 22.5
                rad = math.radians(deg)
                self.shade_spawn_points.append([round(43.0 * math.cos(rad), 3), 0.0, round(43.0 * math.sin(rad), 3)])

    def _get_floor_height(self, x: float, z: float) -> Optional[float]:
        # Returns floor Y, or None if in void (falling)
        if self.night == 1:
            r = math.hypot(x, z)
            if r <= 40.0:
                return 0.0
            return None
        elif self.night == 2:
            r_a = math.hypot(x - 0.0, z - 0.0)
            if r_a <= 28.0:
                return 0.0
            r_b = math.hypot(x - 70.0, z - 0.0)
            if r_b <= 28.0:
                return 0.0
            # Bamboo bridge: x in [26, 44], z in [-2, 2]
            if 26.0 <= x <= 44.0 and -2.0 <= z <= 2.0:
                return 0.0
            return None
        elif self.night == 3:
            r = math.hypot(x, z)
            # Tier 2: disc R <= 8 at Y=6
            if r <= 8.0:
                # Bell tower cylinder at center R <= 2: barrier
                return 6.0
            # Tier 1: ring 12 <= R <= 24 at z > 0, Y=3
            if 12.0 <= r <= 24.0 and z > 0.0:
                return 3.0
            # Check 2 ramps: wide 3m along radial lines at 30 deg and 150 deg, R in [24, 30]
            # Ramp height transitions from Y=0 at R=30 to Y=3 at R=24
            if 24.0 <= r <= 30.0:
                ang_deg = math.degrees(math.atan2(z, x))
                for ramp_ang in [30.0, 150.0]:
                    diff = abs((ang_deg - ramp_ang + 180.0) % 360.0 - 180.0)
                    dist_to_centerline = r * math.sin(math.radians(diff))
                    if abs(dist_to_centerline) <= 1.5:
                        # On ramp
                        t = (30.0 - r) / (30.0 - 24.0) # 0 at R=30, 1 at R=24
                        return 0.0 + t * 3.0
            # Tier 0: full island R <= 45 at Y=0
            if r <= 45.0:
                return 0.0
            return None
        return 0.0

    def apply_scenario(self, scenario: Dict[str, Any]):
        if "player" in scenario:
            p_data = scenario["player"]
            if "pos" in p_data:
                self.player.pos = [float(v) for v in p_data["pos"]]
            if "carried" in p_data:
                self.player.carried = int(p_data["carried"])
            if "flames" in p_data:
                self.player.flames = int(p_data["flames"])
            if "invuln_ticks" in p_data:
                self.player.invuln_ticks = int(p_data["invuln_ticks"])
                self.player.invuln = self.player.invuln_ticks > 0
            if "dash_cd_ticks" in p_data:
                self.player.dash_cd_ticks = int(p_data["dash_cd_ticks"])
            if "pulse_cd_ticks" in p_data:
                self.player.pulse_cd_ticks = int(p_data["pulse_cd_ticks"])
            if "charm_ticks" in p_data:
                self.player.charm_ticks_left = int(p_data["charm_ticks"])

        if "random_motes" in scenario:
            self.random_motes = bool(scenario["random_motes"])
        if "random_shades" in scenario:
            self.random_shades = bool(scenario["random_shades"])
        if "random_drifters" in scenario:
            self.random_drifters = bool(scenario["random_drifters"])
        if "wind_enabled" in scenario:
            self.wind_enabled = bool(scenario["wind_enabled"])

        if "time_left_s" in scenario:
            self.time_left_s = float(scenario["time_left_s"])

        if "lanterns" in scenario:
            for l_in in scenario["lanterns"]:
                lid = l_in.get("id")
                target = next((l for l in self.lanterns if l.id == lid), None)
                if target:
                    if "pos" in l_in:
                        target.pos = [float(v) for v in l_in["pos"]]
                    if "deposited" in l_in:
                        target.deposited = int(l_in["deposited"])
                    if "lit" in l_in:
                        target.lit = bool(l_in["lit"])
                else:
                    self.lanterns.append(LanternState(
                        id=lid,
                        pos=[float(v) for v in l_in.get("pos", [0.0, 0.0, 0.0])],
                        deposited=int(l_in.get("deposited", 0)),
                        lit=bool(l_in.get("lit", False))
                    ))

        if "motes" in scenario:
            self.motes = []
            for i, m_in in enumerate(scenario["motes"]):
                if isinstance(m_in, list):
                    mpos = [float(v) for v in m_in]
                    self.motes.append(MoteState(id=f"M{i+1}", pos=mpos, kind="random"))
                elif isinstance(m_in, dict):
                    mid = m_in.get("id", f"M{i+1}")
                    mpos = [float(v) for v in m_in.get("pos", [0.0, 0.0, 0.0])]
                    kind = m_in.get("kind", "random")
                    ttl_ticks = int(m_in.get("ttl_s", 8.0) * 60) if "ttl_s" in m_in and m_in["ttl_s"] is not None else None
                    self.motes.append(MoteState(id=mid, pos=mpos, kind=kind, ttl_ticks=ttl_ticks))
            self.next_mote_id_idx = len(scenario["motes"]) + 1

        if "shades" in scenario:
            self.shades = []
            for i, s_in in enumerate(scenario["shades"]):
                sid = s_in.get("id", f"S{i+1}")
                pos = [float(v) for v in s_in.get("pos", [10.0, 0.0, 0.0])]
                state = s_in.get("state", "chase")
                ticks_left = int(s_in.get("state_ticks_left", 0))
                self.shades.append(ShadeState(id=sid, pos=pos, state=state, state_ticks_left=ticks_left))
            self.next_shade_id_idx = len(scenario["shades"]) + 1

        if "drifters" in scenario:
            self.drifters = []
            for i, d_in in enumerate(scenario["drifters"]):
                did = d_in.get("id", f"D{i+1}")
                pos = [float(v) for v in d_in.get("pos", [0.0, 0.0, 0.0])]
                state = d_in.get("state", "idle")
                stolen = int(d_in.get("stolen", 0))
                self.drifters.append(DrifterState(id=did, pos=pos, state=state, stolen=stolen))
            self.next_drifter_id_idx = len(scenario["drifters"]) + 1

        if "charms" in scenario:
            self.charms = []
            for i, c_in in enumerate(scenario["charms"]):
                cid = c_in.get("id", f"C{i+1}")
                pos = [float(v) for v in c_in.get("pos", [0.0, 0.0, 0.0])]
                avail = bool(c_in.get("available", True))
                respawn = int(c_in.get("respawn_s", 0.0) * 60)
                self.charms.append(CharmState(id=cid, pos=pos, available=avail, respawn_ticks=respawn))

    def apply_input_frame(self, frame: Dict[str, Any]):
        if "move" in frame:
            self.current_move = [float(frame["move"][0]), float(frame["move"][1])]
        if "cam_yaw_deg" in frame:
            self.current_cam_yaw_deg = float(frame["cam_yaw_deg"])
        if "interact" in frame:
            self.current_interact = bool(frame["interact"])
        if "pulse" in frame:
            self.current_pulse = bool(frame["pulse"])
        if "jump" in frame:
            self.current_jump = bool(frame["jump"])
        if "dash" in frame:
            self.current_dash = bool(frame["dash"])
        if "pause" in frame:
            self.current_pause = bool(frame["pause"])

    def _horizontal_distance(self, p1: List[float], p2: List[float]) -> float:
        return math.hypot(p1[0] - p2[0], p1[2] - p2[2])

    def _dist_3d(self, p1: List[float], p2: List[float]) -> float:
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

    def step(self):
        next_tick = self.tick + 1
        self.events_this_tick = []

        # -------------------------------------------------------------
        # STEP 1: Đọc input & Xử lý pause trước
        # -------------------------------------------------------------
        pause_triggered = self.current_pause and not self.prev_pause
        self.prev_pause = self.current_pause

        if pause_triggered:
            if self.state == "paused":
                self.state = self.prev_state_before_pause
                self.events_this_tick.append({"type": "event", "tick": next_tick, "name": "resumed", "data": {}})
            else:
                self.prev_state_before_pause = self.state
                self.state = "paused"
                self.events_this_tick.append({"type": "event", "tick": next_tick, "name": "paused", "data": {}})
                self.tick = next_tick
                return # Dừng bước tại đây khi vừa tạm dừng

        if self.state == "paused":
            # Khi đang tạm dừng: tick tăng nhưng sim_tick, thời gian, hồi chiêu, spawn, TTL đều đứng yên
            self.tick = next_tick
            return

        if self.state != "playing":
            self.tick = next_tick
            return

        # -------------------------------------------------------------
        # STEP 2: Giảm các bộ đếm
        # thời gian, hồi chiêu, bất tử, choáng, bùa, TTL đom đóm rơi, hồi bùa
        # -------------------------------------------------------------
        self.time_left_s = max(0.0, self.time_left_s - self.dt)

        if self.player.invuln_ticks > 0:
            self.player.invuln_ticks -= 1
        self.player.invuln = (self.player.invuln_ticks > 0)

        if self.player.dash_cd_ticks > 0:
            self.player.dash_cd_ticks -= 1

        if self.player.pulse_cd_ticks > 0:
            self.player.pulse_cd_ticks -= 1

        if self.player.charm_ticks_left > 0:
            self.player.charm_ticks_left -= 1

        # Charm respawn timers
        for charm in self.charms:
            if not charm.available and charm.respawn_ticks > 0:
                charm.respawn_ticks -= 1
                if charm.respawn_ticks <= 0:
                    charm.available = True

        # Mote TTL
        for mote in self.motes:
            if mote.active:
                mote.age_ticks += 1
                if mote.kind == "dropped" and mote.ttl_ticks is not None:
                    mote.ttl_ticks -= 1
                    if mote.ttl_ticks <= 0:
                        mote.active = False

        # Recently lit lanterns protection timer (30 ticks)
        for L in self.lanterns:
            if L.recently_lit_ticks > 0:
                L.recently_lit_ticks -= 1

        # -------------------------------------------------------------
        # STEP 3: Di chuyển Mây (nhảy, lướt, bục nhảy, gió) rồi kiểm tra rơi khỏi đảo
        # -------------------------------------------------------------
        jump_triggered = self.current_jump and not self.prev_jump
        dash_triggered = self.current_dash and not self.prev_dash
        interact_triggered = self.current_interact and not self.prev_interact
        pulse_triggered = self.current_pulse and not self.prev_pulse

        self.prev_jump = self.current_jump
        self.prev_dash = self.current_dash
        self.prev_interact = self.current_interact
        self.prev_pulse = self.current_pulse

        # Fall recovery handling
        if self.player.fall_wait_ticks > 0:
            self.player.fall_wait_ticks -= 1
            if self.player.fall_wait_ticks <= 0:
                # Respawn at (0,0,0)
                self.player.pos = [0.0, 0.0, 0.0]
                self.player.vel = [0.0, 0.0, 0.0]
                self.player.grounded = True
                self.player.invuln_ticks = 90
                self.player.invuln = True
                self.player.jumppad_flight = False
        else:
            # Action: Jump (chỉ nhảy khi chạm đất)
            if jump_triggered and self.player.grounded:
                self.player.vel[1] = 7.0
                self.player.grounded = False

            # Action: Dash
            has_charm = (self.player.charm_ticks_left > 0)
            if dash_triggered and (has_charm or self.player.dash_cd_ticks <= 0) and self.player.dash_ticks_left <= 0:
                self.player.dash_ticks_left = 12 # 0.2s = 12 ticks
                self.player.dash_cd_ticks = 90 # 1.5s = 90 ticks
                # Direction of dash: moving direction if moving, else facing direction
                mag_m = math.hypot(self.current_move[0], self.current_move[1])
                if mag_m > 0.01:
                    theta = math.radians(self.current_cam_yaw_deg)
                    x_in, z_in = self.current_move[0], self.current_move[1]
                    xp = x_in * math.cos(theta) + z_in * math.sin(theta)
                    zp = -x_in * math.sin(theta) + z_in * math.cos(theta)
                    mag_p = math.hypot(xp, zp)
                    self.player.dash_dir = [xp / mag_p, 0.0, zp / mag_p]
                else:
                    self.player.dash_dir = [self.player.facing_dir[0], 0.0, self.player.facing_dir[2]]
                self.events_this_tick.append({"type": "event", "tick": next_tick, "name": "dash", "data": {}})

            # Process Wind in Night 3
            if self.wind_enabled:
                self.wind.cycle_ticks += 1
                if self.wind.cycle_ticks >= 1800: # 30s
                    self.wind.cycle_ticks = 0
                    self.wind.active = True
                    self.wind.duration_ticks = 300 # 5s
                    self.wind.dir_deg = self.rng.uniform(0.0, 360.0)
                    rad_w = math.radians(self.wind.dir_deg)
                    self.wind.wind_vector = [2.0 * math.cos(rad_w), 0.0, 2.0 * math.sin(rad_w)]

                if self.wind.active:
                    self.wind.duration_ticks -= 1
                    if self.wind.duration_ticks <= 0:
                        self.wind.active = False
                        self.wind.wind_vector = [0.0, 0.0, 0.0]

            # Player displacement
            if self.player.dash_ticks_left > 0:
                # Dashing: 14 m/s in dash_dir, maintain height on air
                self.player.pos[0] += self.player.dash_dir[0] * self.tuning.dash_speed * self.dt
                self.player.pos[2] += self.player.dash_dir[2] * self.tuning.dash_speed * self.dt
                self.player.vel[0] = self.player.dash_dir[0] * self.tuning.dash_speed
                self.player.vel[2] = self.player.dash_dir[2] * self.tuning.dash_speed
                self.player.vel[1] = 0.0
                self.player.dash_ticks_left -= 1
            elif self.player.jumppad_flight:
                # Jumppad trajectory: maintain horizontal velocity, gravity -20
                self.player.vel[1] += -20.0 * self.dt
                self.player.pos[0] += self.player.vel[0] * self.dt
                self.player.pos[1] += self.player.vel[1] * self.dt
                self.player.pos[2] += self.player.vel[2] * self.dt
            else:
                # Normal running
                run_speed = 7.2 if has_charm else self.tuning.player_speed
                theta = math.radians(self.current_cam_yaw_deg)
                x_in, z_in = self.current_move[0], self.current_move[1]
                x_prime = x_in * math.cos(theta) + z_in * math.sin(theta)
                z_prime = -x_in * math.sin(theta) + z_in * math.cos(theta)
                mag = math.hypot(x_prime, z_prime)
                if mag > 1.0:
                    x_prime /= mag
                    z_prime /= mag
                if mag > 0.01:
                    self.player.facing_dir = [x_prime / mag, 0.0, z_prime / mag]

                self.player.vel[0] = x_prime * run_speed
                self.player.vel[2] = z_prime * run_speed

                # Add wind
                if self.wind.active:
                    self.player.vel[0] += self.wind.wind_vector[0]
                    self.player.vel[2] += self.wind.wind_vector[2]

                self.player.pos[0] += self.player.vel[0] * self.dt
                self.player.pos[2] += self.player.vel[2] * self.dt

                # Gravity
                if not self.player.grounded:
                    self.player.vel[1] += -20.0 * self.dt
                    self.player.pos[1] += self.player.vel[1] * self.dt

            # Floor and Terrain collision
            floor_y = self._get_floor_height(self.player.pos[0], self.player.pos[2])
            if floor_y is not None:
                if self.player.pos[1] <= floor_y:
                    self.player.pos[1] = floor_y
                    self.player.vel[1] = 0.0
                    self.player.grounded = True
                    self.player.jumppad_flight = False
                elif self.player.dash_ticks_left <= 0 and not self.player.jumppad_flight:
                    # In air above floor
                    self.player.grounded = False
            else:
                # Over void: falling
                self.player.grounded = False
                if not self.player.jumppad_flight and self.player.dash_ticks_left <= 0:
                    self.player.vel[1] += -20.0 * self.dt
                    self.player.pos[1] += self.player.vel[1] * self.dt

            # Check Jump Pad trigger (chỉ khi chân chạm bục XZ <= 1.0m)
            if self.player.grounded or abs(self.player.pos[1] - (floor_y or 0.0)) <= 0.5:
                for pad in self.jump_pads:
                    d_pad = self._horizontal_distance(self.player.pos, pad.pos)
                    if d_pad <= pad.radius:
                        self.player.grounded = False
                        self.player.jumppad_flight = True
                        self.player.vel[1] = pad.launch_vy
                        if pad.target_dir:
                            self.player.vel[0] = pad.target_dir[0] * pad.launch_hspeed
                            self.player.vel[2] = pad.target_dir[2] * pad.launch_hspeed
                        break

            # Fall check: Y < -10
            if self.player.pos[1] < -10.0:
                self.player.flames -= 1
                lost = self.player.carried
                self.player.carried = 0
                self.events_this_tick.append({
                    "type": "event",
                    "tick": next_tick,
                    "name": "player_hit",
                    "data": {
                        "by": "fall",
                        "flames": self.player.flames,
                        "dropped": 0,
                        "lost": lost
                    }
                })
                if self.player.flames <= 0:
                    self.state = "lost"
                    self.events_this_tick.append({
                        "type": "event",
                        "tick": next_tick,
                        "name": "game_over",
                        "data": {"result": "lost", "reason": "no_flames"}
                    })
                else:
                    self.player.fall_wait_ticks = 60
                    self.player.pos = [0.0, 0.0, 0.0]
                    self.player.vel = [0.0, 0.0, 0.0]

        # -------------------------------------------------------------
        # STEP 4: Nhặt đom đóm và bùa
        # -------------------------------------------------------------
        if self.player.fall_wait_ticks <= 0:
            # Pick motes
            for mote in self.motes:
                if mote.active:
                    d_xz = self._horizontal_distance(self.player.pos, mote.pos)
                    d_y = abs(self.player.pos[1] - mote.pos[1])
                    if d_xz <= self.tuning.pickup_radius and d_y <= 1.5:
                        if mote.kind == "dropped" and mote.age_ticks < 1:
                            continue # Nhặt lại được từ tick sau
                        if self.player.carried < self.tuning.carry_capacity:
                            mote.active = False
                            self.player.carried += 1
                            self.events_this_tick.append({
                                "type": "event",
                                "tick": next_tick,
                                "name": "mote_picked",
                                "data": {"carried": self.player.carried}
                            })

            # Pick charms
            for charm in self.charms:
                if charm.available:
                    d_xz = self._horizontal_distance(self.player.pos, charm.pos)
                    d_y = abs(self.player.pos[1] - charm.pos[1])
                    if d_xz <= 1.0 and d_y <= 1.5:
                        charm.available = False
                        charm.respawn_ticks = 2700
                        self.player.charm_ticks_left = 600
                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "charm_picked",
                            "data": {
                                "charm_id": charm.id,
                                "charm_ticks": 600
                            }
                        })

        # -------------------------------------------------------------
        # STEP 5: Tương tác với đèn
        # -------------------------------------------------------------
        if interact_triggered and self.player.carried > 0 and self.player.fall_wait_ticks <= 0:
            unlit_in_range = []
            for L in self.lanterns:
                if not L.lit:
                    d = self._horizontal_distance(self.player.pos, L.pos)
                    if d <= self.tuning.interact_radius:
                        unlit_in_range.append((d, L.id, L))
            if unlit_in_range:
                unlit_in_range.sort(key=lambda item: (item[0], item[1]))
                target_l = unlit_in_range[0][2]
                needed = self.tuning.lantern_cost - target_l.deposited
                deposit_amt = min(self.player.carried, needed)
                if deposit_amt > 0:
                    self.player.carried -= deposit_amt
                    target_l.deposited += deposit_amt
                    self.score += deposit_amt * self.tuning.per_mote_score
                    self.events_this_tick.append({
                        "type": "event",
                        "tick": next_tick,
                        "name": "deposit",
                        "data": {
                            "lantern_id": target_l.id,
                            "amount": deposit_amt,
                            "deposited": target_l.deposited
                        }
                    })
                    if target_l.deposited >= self.tuning.lantern_cost:
                        target_l.lit = True
                        target_l.recently_lit_ticks = 30
                        self.score += self.tuning.per_lantern_score
                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "lantern_lit",
                            "data": {"lantern_id": target_l.id}
                        })

        # -------------------------------------------------------------
        # STEP 6: Cập nhật vùng an toàn
        # -------------------------------------------------------------
        # Lit lanterns push or block shades in 6m radius
        for shade in self.shades:
            if shade.state == "spawning":
                continue
            for L in self.lanterns:
                if L.lit:
                    d_l = self._horizontal_distance(shade.pos, L.pos)
                    if d_l < self.tuning.safe_radius:
                        # Push outside to edge 6m + epsilon
                        if d_l > 0.001:
                            dx = (shade.pos[0] - L.pos[0]) / d_l
                            dz = (shade.pos[2] - L.pos[2]) / d_l
                        else:
                            dx, dz = 1.0, 0.0
                        shade.pos[0] = L.pos[0] + dx * (self.tuning.safe_radius + 0.1)
                        shade.pos[2] = L.pos[2] + dz * (self.tuning.safe_radius + 0.1)

        # -------------------------------------------------------------
        # STEP 7: Tỏa Sáng
        # -------------------------------------------------------------
        if pulse_triggered and self.player.carried >= self.tuning.pulse_cost and self.player.pulse_cd_ticks <= 0 and self.player.fall_wait_ticks <= 0:
            self.player.carried -= self.tuning.pulse_cost
            self.player.pulse_cd_ticks = int(self.tuning.pulse_cooldown_s * 60) # 180 ticks
            pulse_center = [self.player.pos[0], self.player.pos[1] + 0.8, self.player.pos[2]]

            stunned_ids = []
            for shade in self.shades:
                d3 = self._dist_3d(pulse_center, shade.pos)
                if d3 <= self.tuning.pulse_radius:
                    shade.state = "stunned"
                    shade.state_ticks_left = 120 # 2.0s
                    shade.push_ticks_left = 15
                    dh = self._horizontal_distance(self.player.pos, shade.pos)
                    if dh > 0.001:
                        shade.push_dir = [(shade.pos[0] - self.player.pos[0]) / dh, (shade.pos[2] - self.player.pos[2]) / dh]
                    else:
                        shade.push_dir = [1.0, 0.0]
                    stunned_ids.append(shade.id)
                    self.score += self.tuning.per_stun_score

            # Check drifters affected by pulse
            for drifter in self.drifters:
                if drifter.state in ["chase", "flee"]:
                    d3 = self._dist_3d(pulse_center, drifter.pos)
                    if d3 <= self.tuning.pulse_radius:
                        if drifter.state == "chase":
                            drifter.state = "flee"
                            drifter.state_ticks_left = 240
                            dh = self._horizontal_distance(self.player.pos, drifter.pos)
                            if dh > 0.001:
                                drifter.flee_dir = [(drifter.pos[0] - self.player.pos[0]) / dh, 0.0, (drifter.pos[2] - self.player.pos[2]) / dh]
                            else:
                                drifter.flee_dir = [1.0, 0.0, 0.0]
                        elif drifter.state == "flee" and drifter.stolen > 0:
                            # Drop stolen motes on spot
                            amt = drifter.stolen
                            drifter.stolen = 0
                            for _ in range(amt):
                                self.motes.append(MoteState(
                                    id=f"M{self.next_mote_id_idx}",
                                    pos=[drifter.pos[0], drifter.pos[1], drifter.pos[2]],
                                    kind="dropped",
                                    ttl_ticks=480
                                ))
                                self.next_mote_id_idx += 1
                            self.events_this_tick.append({
                                "type": "event",
                                "tick": next_tick,
                                "name": "drifter_drop",
                                "data": {"drifter_id": drifter.id, "amount": amt}
                            })
                            drifter.state_ticks_left = 120

            self.events_this_tick.append({
                "type": "event",
                "tick": next_tick,
                "name": "pulse",
                "data": {"stunned_ids": stunned_ids}
            })

        # -------------------------------------------------------------
        # STEP 8: Di chuyển Bóng Mực và Gió Lạc
        # -------------------------------------------------------------
        shade_speed = 4.5 if self.night == 3 else self.tuning.shade_speed

        for shade in self.shades:
            if shade.state == "stunned":
                if shade.push_ticks_left > 0:
                    step_push = (self.tuning.pulse_push_m / 15.0)
                    shade.pos[0] += shade.push_dir[0] * step_push
                    shade.pos[2] += shade.push_dir[1] * step_push
                    shade.push_ticks_left -= 1
                shade.state_ticks_left -= 1
                if shade.state_ticks_left <= 0:
                    shade.state = "wander"
            elif shade.state == "recoil":
                step_recoil = (2.0 / 60.0)
                shade.pos[0] += shade.recoil_dir[0] * step_recoil
                shade.pos[2] += shade.recoil_dir[1] * step_recoil
                shade.state_ticks_left -= 1
                if shade.state_ticks_left <= 0:
                    shade.state = "chase"
            elif shade.state == "spawning":
                shade.state_ticks_left -= 1
                if shade.state_ticks_left <= 0:
                    shade.state = "wander"
            else:
                # wander or chase
                d_p = self._horizontal_distance(shade.pos, self.player.pos)
                if d_p <= 12.0:
                    shade.state = "chase"
                elif d_p > 18.0:
                    shade.state = "wander"

                if shade.state == "chase":
                    if d_p > 0.001:
                        dx = (self.player.pos[0] - shade.pos[0]) / d_p
                        dz = (self.player.pos[2] - shade.pos[2]) / d_p
                        new_x = shade.pos[0] + dx * shade_speed * self.dt
                        new_z = shade.pos[2] + dz * shade_speed * self.dt

                        # Safe zone check
                        blocked = False
                        for L in self.lanterns:
                            if L.lit:
                                if math.hypot(new_x - L.pos[0], new_z - L.pos[2]) < self.tuning.safe_radius:
                                    blocked = True
                                    break
                        if not blocked:
                            shade.pos[0] = new_x
                            shade.pos[2] = new_z

        # Move Drifters
        for drifter in self.drifters:
            if drifter.state == "removed":
                continue
            elif drifter.state == "idle":
                # Glide slowly at 2.0 m/s
                d_p = self._horizontal_distance(drifter.pos, self.player.pos)
                if self.player.carried >= 5 and d_p <= 15.0:
                    drifter.state = "chase"
            elif drifter.state == "chase":
                d_p = self._horizontal_distance(drifter.pos, self.player.pos)
                if self.player.carried < 5 or d_p > 15.0:
                    drifter.state = "idle"
                else:
                    if d_p > 0.001:
                        dx = (self.player.pos[0] - drifter.pos[0]) / d_p
                        dz = (self.player.pos[2] - drifter.pos[2]) / d_p
                        drifter.pos[0] += dx * 7.0 * self.dt
                        drifter.pos[2] += dz * 7.0 * self.dt
            elif drifter.state == "flee":
                drifter.pos[0] += drifter.flee_dir[0] * 7.0 * self.dt
                drifter.pos[2] += drifter.flee_dir[2] * 7.0 * self.dt
                drifter.state_ticks_left -= 1
                if drifter.state_ticks_left <= 0:
                    drifter.state = "removed"

        # -------------------------------------------------------------
        # STEP 9: Chạm
        # Gió Lạc cướp trước, rồi Bóng Mực gây hit (xét theo id tăng dần)
        # -------------------------------------------------------------
        if self.player.fall_wait_ticks <= 0:
            # Drifter steal
            for drifter in self.drifters:
                if drifter.state == "chase" and not drifter.has_stolen_once:
                    d_xz = self._horizontal_distance(drifter.pos, self.player.pos)
                    if d_xz <= 1.2:
                        amt = min(3, self.player.carried)
                        self.player.carried -= amt
                        drifter.stolen = amt
                        drifter.has_stolen_once = True
                        drifter.state = "flee"
                        drifter.state_ticks_left = 240
                        d_h = self._horizontal_distance(self.player.pos, drifter.pos)
                        if d_h > 0.001:
                            drifter.flee_dir = [(drifter.pos[0] - self.player.pos[0]) / d_h, 0.0, (drifter.pos[2] - self.player.pos[2]) / d_h]
                        else:
                            drifter.flee_dir = [1.0, 0.0, 0.0]
                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "drifter_steal",
                            "data": {
                                "drifter_id": drifter.id,
                                "amount": amt,
                                "carried": self.player.carried
                            }
                        })

            # Shade hit (sorted by id ascending)
            sorted_shades = sorted(self.shades, key=lambda s: s.id)
            hit_this_tick = False
            for shade in sorted_shades:
                if shade.state in ["spawning", "stunned"]:
                    continue
                d_xz = self._horizontal_distance(shade.pos, self.player.pos)
                d_y = abs(shade.pos[1] - self.player.pos[1])
                if d_xz <= self.tuning.shade_hit_radius and d_y <= 1.5:
                    # Recoil
                    shade.state = "recoil"
                    shade.state_ticks_left = 60
                    if d_xz > 0.001:
                        shade.recoil_dir = [(shade.pos[0] - self.player.pos[0]) / d_xz, (shade.pos[2] - self.player.pos[2]) / d_xz]
                    else:
                        shade.recoil_dir = [1.0, 0.0]

                    if not self.player.invuln and not hit_this_tick:
                        hit_this_tick = True
                        self.player.flames -= 1
                        dropped = int(self.player.carried * self.tuning.hit_drop_ratio)
                        self.player.carried -= dropped
                        self.player.invuln_ticks = 90
                        self.player.invuln = True

                        # Drop motes in ring 1.5 - 2.5m around player
                        for _ in range(dropped):
                            ang = self.rng.uniform(0.0, 2.0 * math.pi)
                            dist = self.rng.uniform(1.5, 2.5)
                            m_pos = [self.player.pos[0] + dist * math.cos(ang), self.player.pos[1], self.player.pos[2] + dist * math.sin(ang)]
                            self.motes.append(MoteState(
                                id=f"M{self.next_mote_id_idx}",
                                pos=m_pos,
                                kind="dropped",
                                ttl_ticks=480
                            ))
                            self.next_mote_id_idx += 1

                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "player_hit",
                            "data": {
                                "by": "shade",
                                "flames": self.player.flames,
                                "dropped": dropped
                            }
                        })

        # -------------------------------------------------------------
        # STEP 10: Sinh đom đóm, Bóng Mực, Gió Lạc theo lịch
        # Thực thể mới chỉ tương tác được từ tick sau
        # -------------------------------------------------------------
        if self.random_motes:
            # Every 240 ticks, spawn 1 mote at an empty spawn point if active < 30
            active_motes_cnt = sum(1 for m in self.motes if m.active)
            if self.sim_tick > 0 and self.sim_tick % 240 == 0 and active_motes_cnt < 30:
                # Find an empty spawn point
                occupied_pts = [m.pos for m in self.motes if m.active]
                available_pts = []
                for pt in self.mote_spawn_points:
                    if not any(math.hypot(pt[0] - op[0], pt[2] - op[2]) < 1.0 for op in occupied_pts):
                        available_pts.append(pt)
                if available_pts:
                    pt = self.rng.choice(available_pts)
                    self.motes.append(MoteState(id=f"M{self.next_mote_id_idx}", pos=[pt[0], pt[1], pt[2]], kind="random"))
                    self.next_mote_id_idx += 1

        if self.random_shades:
            # Spawn shades: 2 at tick 300, then 1 every interval
            max_shades = 6 if self.night == 1 else (8 if self.night == 2 else 10)
            spawn_interval = 480 if self.night == 1 else (420 if self.night == 2 else 360)
            active_shades_cnt = len(self.shades)

            to_spawn = 0
            if self.sim_tick == 300 and active_shades_cnt < max_shades:
                to_spawn = min(2, max_shades - active_shades_cnt)
            elif self.sim_tick > 300 and (self.sim_tick - 300) % spawn_interval == 0 and active_shades_cnt < max_shades:
                to_spawn = 1

            for _ in range(to_spawn):
                valid_pts = [pt for pt in self.shade_spawn_points if self._horizontal_distance(self.player.pos, pt) >= 15.0]
                if valid_pts:
                    pt = self.rng.choice(valid_pts)
                    sid = f"S{self.next_shade_id_idx}"
                    self.next_shade_id_idx += 1
                    self.shades.append(ShadeState(id=sid, pos=[pt[0], pt[1], pt[2]], state="chase"))
                    self.events_this_tick.append({
                        "type": "event",
                        "tick": next_tick,
                        "name": "shade_spawned",
                        "data": {"id": sid}
                    })

        if self.random_drifters and self.night in [2, 3]:
            # Spawn drifters: at tick 1200, 2400... max 2 active
            active_drifters = [d for d in self.drifters if d.state != "removed"]
            if self.sim_tick > 0 and self.sim_tick % 1200 == 0 and len(active_drifters) < 2:
                did = f"D{self.next_drifter_id_idx}"
                self.next_drifter_id_idx += 1
                spawn_r = 30.0 if self.night == 2 else 40.0
                ang = self.rng.uniform(0.0, 2.0 * math.pi)
                self.drifters.append(DrifterState(
                    id=did,
                    pos=[spawn_r * math.cos(ang), 2.0, spawn_r * math.sin(ang)],
                    state="idle"
                ))

        # -------------------------------------------------------------
        # STEP 11: Xét thắng/thua
        # -------------------------------------------------------------
        all_lit = len(self.lanterns) > 0 and all(L.lit for L in self.lanterns)
        if self.player.flames <= 0:
            if self.state == "playing":
                self.state = "lost"
                self.events_this_tick.append({
                    "type": "event",
                    "tick": next_tick,
                    "name": "game_over",
                    "data": {"result": "lost", "reason": "no_flames"}
                })
        elif all_lit:
            if self.state == "playing":
                self.state = "won"
                win_time_bonus = math.floor(self.time_left_s) * self.tuning.per_second_left_score
                win_flame_bonus = self.player.flames * self.tuning.per_flame_left_score
                self.score += win_time_bonus + win_flame_bonus
                self.events_this_tick.append({
                    "type": "event",
                    "tick": next_tick,
                    "name": "game_over",
                    "data": {"result": "won", "reason": "all_lit"}
                })
        elif self.time_left_s <= 0:
            if self.state == "playing":
                self.state = "lost"
                self.events_this_tick.append({
                    "type": "event",
                    "tick": next_tick,
                    "name": "game_over",
                    "data": {"result": "lost", "reason": "dawn"}
                })

        # -------------------------------------------------------------
        # STEP 12: Hoàn tất tick
        # -------------------------------------------------------------
        self.tick = next_tick
        self.sim_tick += 1

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "type": "snapshot",
            "tick": self.tick,
            "sim_tick": self.sim_tick,
            "state": self.state,
            "night": self.night,
            "time_left_s": round(self.time_left_s, 3),
            "score": self.score,
            "wind": {
                "active": self.wind.active,
                "dir_deg": round(self.wind.dir_deg, 3)
            },
            "player": {
                "pos": [round(v, 3) for v in self.player.pos],
                "vel": [round(v, 3) for v in self.player.vel],
                "grounded": self.player.grounded,
                "invuln": self.player.invuln,
                "flames": self.player.flames,
                "carried": self.player.carried,
                "dash_cd_s": round(self.player.dash_cd_ticks / 60.0, 3),
                "pulse_cd_s": round(self.player.pulse_cd_ticks / 60.0, 3),
                "charm_s": round(self.player.charm_ticks_left / 60.0, 3)
            },
            "lanterns": [
                {
                    "id": L.id,
                    "pos": [round(v, 3) for v in L.pos],
                    "lit": L.lit,
                    "deposited": L.deposited
                }
                for L in self.lanterns
            ],
            "shades": [
                {
                    "id": s.id,
                    "pos": [round(v, 3) for v in s.pos],
                    "state": s.state
                }
                for s in self.shades
            ],
            "motes": [
                {
                    "id": m.id,
                    "pos": [round(v, 3) for v in m.pos],
                    "kind": m.kind,
                    "ttl_s": round(m.ttl_ticks / 60.0, 3) if m.ttl_ticks is not None else None
                }
                for m in self.motes
                if m.active
            ],
            "drifters": [
                {
                    "id": d.id,
                    "pos": [round(v, 3) for v in d.pos],
                    "state": d.state,
                    "stolen": d.stolen
                }
                for d in self.drifters
                if d.state != "removed"
            ],
            "charms": [
                {
                    "id": c.id,
                    "available": c.available,
                    "respawn_s": round(c.respawn_ticks / 60.0, 3)
                }
                for c in self.charms
            ],
            "motes_active": sum(1 for m in self.motes if m.active)
        }

    def get_end_record(self) -> Dict[str, Any]:
        return {
            "type": "end",
            "ticks": self.tick,
            "state": self.state,
            "score": self.score
        }
