import argparse
import json
import math
import random
import sys
import time
import psutil
from typing import List, Dict, Any, Optional
from src.core.models import Tuning
from src.core.engine import SimulationEngine

def run_soak_test(args_list: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Dao Den Long Soak Test Runner (Contract v1.3)")
    parser.add_argument("--seed", type=int, default=7, help="Initial RNG seed")
    parser.add_argument("--nights", type=int, default=10, help="Number of consecutive nights to simulate")
    parser.add_argument("--out", type=str, default="soak.json", help="Output JSON path")

    parsed_args = parser.parse_args(args_list)

    total_nights = parsed_args.nights
    initial_seed = parsed_args.seed
    results: List[str] = []
    crashes = 0

    proc = psutil.Process()
    mem_start_mb: Optional[int] = None
    t_start = time.time()

    # Shared tuning across nights
    tuning = Tuning()
    try:
        with open("game.contract.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            if "tuning" in c_data:
                for k, v in c_data["tuning"].items():
                    if hasattr(tuning, k) and v is not None:
                        setattr(tuning, k, v)
    except Exception:
        pass

    for night_idx in range(total_nights):
        # Rotate nights: 1 -> 2 -> 3 -> 1 -> 2 -> 3 ...
        night_num = (night_idx % 3) + 1
        current_seed = initial_seed + night_idx
        night_rng = random.Random(current_seed)

        try:
            engine = SimulationEngine(seed=current_seed, tuning=tuning, night=night_num)

            # Record mem_start_mb right after loading first night
            if night_idx == 0:
                mem_start_mb = int(proc.memory_info().rss / (1024 * 1024))

            # Simulate full night up to total duration in ticks
            max_ticks = int(engine.total_duration_s * 60)
            move_dir = [0.0, 0.0]

            for tick in range(max_ticks):
                if engine.state in ["won", "lost"]:
                    break

                # Every 30 ticks: choose new move direction
                if tick % 30 == 0:
                    ang = night_rng.uniform(0.0, 2.0 * math.pi)
                    move_dir = [math.cos(ang), math.sin(ang)]
                engine.current_move = move_dir

                # Probabilistic actions
                engine.current_jump = (night_rng.random() < 0.05)
                engine.current_dash = (night_rng.random() < 0.03)
                engine.current_pulse = (night_rng.random() < 0.02)
                engine.current_interact = (night_rng.random() < 0.10)

                engine.step()

            # Record final outcome of the night
            results.append(engine.state if engine.state in ["won", "lost"] else "playing")

        except Exception as e:
            crashes += 1
            sys.stderr.write(f"Crash occurred during night {night_idx+1}: {e}\n")
            results.append("crashed")

    # Measure mem_end_mb after resetting/finishing the last night
    mem_end_mb = int(proc.memory_info().rss / (1024 * 1024))
    if mem_start_mb is None:
        mem_start_mb = mem_end_mb

    duration_s = round(time.time() - t_start, 1)

    result_data = {
        "nights": total_nights,
        "crashes": crashes,
        "results": results,
        "mem_start_mb": mem_start_mb,
        "mem_end_mb": mem_end_mb,
        "duration_s": duration_s
    }

    try:
        with open(parsed_args.out, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)
    except Exception as e:
        sys.stderr.write(f"Error writing soak test output {parsed_args.out}: {e}\n")
        return 1

    print(f"Soak test completed: nights={total_nights}, crashes={crashes}, mem_start={mem_start_mb}MB, mem_end={mem_end_mb}MB, duration={duration_s}s")
    return 0
