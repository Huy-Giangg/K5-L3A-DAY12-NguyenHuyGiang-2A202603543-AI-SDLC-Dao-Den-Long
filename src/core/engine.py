import math
import random
from typing import List, Dict, Any, Optional, Tuple
from src.core.models import Tuning, PlayerState, LanternState, ShadeState, MoteState

class SimulationEngine:
    def __init__(self, seed: int = 42, tuning: Optional[Tuning] = None):
        self.seed = seed
        self.rng = random.Random(seed)
        self.tuning = tuning or Tuning()
        self.dt = 1.0 / 60.0 # 60 ticks per second

        self.tick = 0
        self.sim_tick = 0
        self.state = "playing" # "playing", "won", "lost"
        self.score = 0
        self.time_left_s = float(self.tuning.night1_duration_s)

        self.player = PlayerState(flames=self.tuning.flames)
        self.lanterns: List[LanternState] = []
        self.shades: List[ShadeState] = []
        self.motes: List[MoteState] = []

        self.random_motes = True
        self.random_shades = True
        self.next_shade_id_idx = 1
        self.next_mote_id_idx = 1

        self.events_this_tick: List[Dict[str, Any]] = []

        # Previous frame button states for edge detection (false -> true)
        self.prev_interact = False
        self.prev_pulse = False
        self.prev_jump = False

        # Current control state
        self.current_move = [0.0, 0.0]
        self.current_cam_yaw_deg = 0.0
        self.current_interact = False
        self.current_pulse = False
        self.current_jump = False

        self._init_default_world()

    def _init_default_world(self):
        # 5 lanterns positioned in circle on island of radius ~30-35m
        island_radius = 25.0
        angles = [0.0, 72.0, 144.0, 216.0, 288.0]
        for i, deg in enumerate(angles):
            rad = math.radians(deg)
            x = island_radius * math.sin(rad)
            z = island_radius * math.cos(rad)
            self.lanterns.append(LanternState(id=f"L{i+1}", pos=[round(x, 3), 0.0, round(z, 3)]))

        # Default motes
        for i in range(20):
            r = self.rng.uniform(5.0, 30.0)
            theta = self.rng.uniform(0.0, 2.0 * math.pi)
            x = r * math.cos(theta)
            z = r * math.sin(theta)
            self.motes.append(MoteState(id=f"M{i+1}", pos=[round(x, 3), 0.0, round(z, 3)]))
        self.next_mote_id_idx = 21

        # Default shades
        for i in range(3):
            r = self.rng.uniform(20.0, 32.0)
            theta = self.rng.uniform(0.0, 2.0 * math.pi)
            x = r * math.cos(theta)
            z = r * math.sin(theta)
            self.shades.append(ShadeState(id=f"S{i+1}", pos=[round(x, 3), 0.0, round(z, 3)]))
        self.next_shade_id_idx = 4

    def apply_scenario(self, scenario: Dict[str, Any]):
        if "player" in scenario:
            p_data = scenario["player"]
            if "pos" in p_data:
                self.player.pos = [float(v) for v in p_data["pos"]]
            if "carried" in p_data:
                self.player.carried = int(p_data["carried"])
            if "flames" in p_data:
                self.player.flames = int(p_data["flames"])

        if "random_motes" in scenario:
            self.random_motes = bool(scenario["random_motes"])
        if "random_shades" in scenario:
            self.random_shades = bool(scenario["random_shades"])

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
            for i, m_pos in enumerate(scenario["motes"]):
                self.motes.append(MoteState(id=f"M{i+1}", pos=[float(v) for v in m_pos]))
            self.next_mote_id_idx = len(scenario["motes"]) + 1

        if "shades" in scenario:
            self.shades = []
            for i, s_in in enumerate(scenario["shades"]):
                sid = s_in.get("id", f"S{i+1}")
                pos = [float(v) for v in s_in.get("pos", [10.0, 0.0, 0.0])]
                self.shades.append(ShadeState(id=sid, pos=pos, state="chase"))
            self.next_shade_id_idx = len(scenario["shades"]) + 1

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

    def _horizontal_distance(self, p1: List[float], p2: List[float]) -> float:
        return math.hypot(p1[0] - p2[0], p1[2] - p2[2])

    def step(self):
        if self.state != "playing":
            return

        self.events_this_tick = []
        next_tick = self.tick + 1

        # 1. Update time
        self.time_left_s = max(0.0, self.time_left_s - self.dt)

        # 2. Movement
        theta = math.radians(self.current_cam_yaw_deg)
        x_in, z_in = self.current_move[0], self.current_move[1]
        x_prime = x_in * math.cos(theta) + z_in * math.sin(theta)
        z_prime = -x_in * math.sin(theta) + z_in * math.cos(theta)

        mag = math.hypot(x_prime, z_prime)
        if mag > 1.0:
            x_prime /= mag
            z_prime /= mag

        self.player.pos[0] += x_prime * self.tuning.player_speed * self.dt
        self.player.pos[2] += z_prime * self.tuning.player_speed * self.dt

        # Check island boundary
        dist_center = math.hypot(self.player.pos[0], self.player.pos[2])
        island_bound = 35.0
        if not self.tuning.fall_enabled and dist_center > island_bound:
            # clamp inside island
            self.player.pos[0] = (self.player.pos[0] / dist_center) * island_bound
            self.player.pos[2] = (self.player.pos[2] / dist_center) * island_bound

        # 3. Handle Actions (Edge Detection: false -> true)
        interact_triggered = self.current_interact and not self.prev_interact
        pulse_triggered = self.current_pulse and not self.prev_pulse

        self.prev_interact = self.current_interact
        self.prev_pulse = self.current_pulse
        self.prev_jump = self.current_jump

        # Action: Deposit into lantern
        if interact_triggered and self.player.carried > 0:
            # Find closest unlit lantern within interact_radius
            closest_lantern = None
            closest_dist = float('inf')
            for L in self.lanterns:
                if not L.lit:
                    d = self._horizontal_distance(self.player.pos, L.pos)
                    if d <= self.tuning.interact_radius and d < closest_dist:
                        closest_lantern = L
                        closest_dist = d

            if closest_lantern:
                needed = self.tuning.lantern_cost - closest_lantern.deposited
                deposit_amt = min(self.player.carried, needed)
                if deposit_amt > 0:
                    self.player.carried -= deposit_amt
                    closest_lantern.deposited += deposit_amt
                    self.events_this_tick.append({
                        "type": "event",
                        "tick": next_tick,
                        "name": "deposit",
                        "data": {
                            "lantern_id": closest_lantern.id,
                            "amount": deposit_amt,
                            "deposited": closest_lantern.deposited
                        }
                    })
                    if closest_lantern.deposited >= self.tuning.lantern_cost:
                        closest_lantern.lit = True
                        self.score += self.tuning.per_lantern_score
                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "lantern_lit",
                            "data": {"lantern_id": closest_lantern.id}
                        })

        # Action: Pulse
        if pulse_triggered and self.player.carried >= self.tuning.pulse_cost and self.player.pulse_cooldown <= 0:
            self.player.carried -= self.tuning.pulse_cost
            self.player.pulse_cooldown = self.tuning.pulse_cooldown_s
            stunned_ids = []
            for shade in self.shades:
                d = self._horizontal_distance(self.player.pos, shade.pos)
                if d <= self.tuning.pulse_radius:
                    shade.state = "stunned"
                    shade.stun_timer = self.tuning.pulse_stun_s
                    # Push back away from player
                    if d > 0.001:
                        dx = (shade.pos[0] - self.player.pos[0]) / d
                        dz = (shade.pos[2] - self.player.pos[2]) / d
                    else:
                        dx, dz = 1.0, 0.0
                    shade.pos[0] += dx * self.tuning.pulse_push_m
                    shade.pos[2] += dz * self.tuning.pulse_push_m
                    stunned_ids.append(shade.id)
                    self.score += self.tuning.per_stun_score

            self.events_this_tick.append({
                "type": "event",
                "tick": next_tick,
                "name": "pulse",
                "data": {"stunned_ids": stunned_ids}
            })

        # 4. Mote pickup
        for mote in self.motes:
            if mote.active:
                d = self._horizontal_distance(self.player.pos, mote.pos)
                if d <= self.tuning.pickup_radius:
                    if self.player.carried < self.tuning.carry_capacity:
                        mote.active = False
                        self.player.carried += 1
                        self.score += self.tuning.per_mote_score
                        self.events_this_tick.append({
                            "type": "event",
                            "tick": next_tick,
                            "name": "mote_picked",
                            "data": {"carried": self.player.carried}
                        })

        # 5. Shades logic
        for shade in self.shades:
            if shade.state == "stunned":
                shade.stun_timer -= self.dt
                if shade.stun_timer <= 0:
                    shade.state = "chase"
            else:
                # Safe zone repulsion by lit lanterns
                in_safe = False
                for L in self.lanterns:
                    if L.lit:
                        dl = self._horizontal_distance(shade.pos, L.pos)
                        if dl <= self.tuning.safe_radius:
                            in_safe = True
                            if dl > 0.001:
                                dx = (shade.pos[0] - L.pos[0]) / dl
                                dz = (shade.pos[2] - L.pos[2]) / dl
                            else:
                                dx, dz = 1.0, 0.0
                            shade.pos[0] = L.pos[0] + dx * (self.tuning.safe_radius + 0.1)
                            shade.pos[2] = L.pos[2] + dz * (self.tuning.safe_radius + 0.1)
                            break

                if not in_safe:
                    dp = self._horizontal_distance(shade.pos, self.player.pos)
                    if dp > 0.001:
                        dx = (self.player.pos[0] - shade.pos[0]) / dp
                        dz = (self.player.pos[2] - shade.pos[2]) / dp
                        shade.pos[0] += dx * self.tuning.shade_speed * self.dt
                        shade.pos[2] += dz * self.tuning.shade_speed * self.dt

                # Collision check with player
                dp = self._horizontal_distance(shade.pos, self.player.pos)
                if dp <= self.tuning.shade_hit_radius:
                    if self.player.invuln_timer <= 0:
                        self.player.flames -= 1
                        dropped = int(self.player.carried * self.tuning.hit_drop_ratio)
                        self.player.carried -= dropped
                        self.player.invuln_timer = self.tuning.invuln_s
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

        # 6. Cooldown timers
        if self.player.invuln_timer > 0:
            self.player.invuln_timer = max(0.0, self.player.invuln_timer - self.dt)
        if self.player.pulse_cooldown > 0:
            self.player.pulse_cooldown = max(0.0, self.player.pulse_cooldown - self.dt)

        # 7. Check Game Over conditions
        all_lit = len(self.lanterns) > 0 and all(L.lit for L in self.lanterns)
        if all_lit:
            self.state = "won"
            time_bonus = int(self.time_left_s) * self.tuning.per_second_left_score
            flame_bonus = self.player.flames * self.tuning.per_flame_left_score
            self.score += time_bonus + flame_bonus
            self.events_this_tick.append({
                "type": "event",
                "tick": next_tick,
                "name": "game_over",
                "data": {"result": "won", "reason": "all_lit"}
            })
        elif self.player.flames <= 0:
            self.state = "lost"
            self.events_this_tick.append({
                "type": "event",
                "tick": next_tick,
                "name": "game_over",
                "data": {"result": "lost", "reason": "no_flames"}
            })
        elif self.time_left_s <= 0:
            self.state = "lost"
            self.events_this_tick.append({
                "type": "event",
                "tick": next_tick,
                "name": "game_over",
                "data": {"result": "lost", "reason": "dawn"}
            })

        self.tick = next_tick
        self.sim_tick = self.tick

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "type": "snapshot",
            "tick": self.tick,
            "sim_tick": self.sim_tick,
            "state": self.state,
            "time_left_s": round(self.time_left_s, 3),
            "score": self.score,
            "player": {
                "pos": [round(v, 3) for v in self.player.pos],
                "flames": self.player.flames,
                "carried": self.player.carried
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
            "motes_active": sum(1 for m in self.motes if m.active)
        }

    def get_end_record(self) -> Dict[str, Any]:
        return {
            "type": "end",
            "ticks": self.tick,
            "state": self.state,
            "score": self.score
        }

