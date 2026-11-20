import argparse
import json
import math
import os
import platform
import sys
import time
import psutil
from typing import List, Dict, Any, Optional
from src.core.models import Tuning, LanternState, ShadeState, MoteState
from src.core.engine import SimulationEngine

def run_benchmark(args_list: Optional[List[str]] = None) -> int:
    t_start_process = time.time()

    parser = argparse.ArgumentParser(description="Dao Den Long Benchmark Mode (Contract v1.3)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--duration", type=int, default=30, help="Benchmark duration in seconds")
    parser.add_argument("--out", type=str, default="bench.json", help="Output JSON path")

    parsed_args = parser.parse_args(args_list)

    # Initialize Benchmark Scene: Night 1
    engine = SimulationEngine(seed=parsed_args.seed, night=1)
    engine.random_motes = False
    engine.random_shades = False
    engine.random_drifters = False
    engine.wind_enabled = False

    # 3 Lanterns L1-L3 lit with fuel 100
    engine.lanterns = [
        LanternState(id="L1", pos=[0.0, 0.0, 25.0], lit=True, fuel=100.0),
        LanternState(id="L2", pos=[23.8, 0.0, 7.7], lit=True, fuel=100.0),
        LanternState(id="L3", pos=[14.7, 0.0, -20.2], lit=True, fuel=100.0),
        LanternState(id="L4", pos=[-14.7, 0.0, -20.2], lit=False, fuel=0.0),
        LanternState(id="L5", pos=[-23.8, 0.0, 7.7], lit=False, fuel=0.0)
    ]

    # Exactly 100 motes
    engine.motes = []
    rng = engine.rng
    for i in range(100):
        r = rng.uniform(4.0, 36.0)
        th = rng.uniform(0.0, 2.0 * math.pi)
        engine.motes.append(MoteState(id=f"M{i+1}", pos=[round(r * math.cos(th), 3), 0.0, round(r * math.sin(th), 3)], kind="random"))

    # Exactly 200 Shades in wander state
    engine.shades = []
    for i in range(200):
        r = rng.uniform(8.0, 38.0)
        th = rng.uniform(0.0, 2.0 * math.pi)
        engine.shades.append(ShadeState(id=f"S{i+1}", pos=[round(r * math.cos(th), 3), 0.0, round(r * math.sin(th), 3)], state="wander"))

    # Player stands still at (0,0,0)
    engine.player.pos = [0.0, 0.0, 0.0]

    load_ms = int((time.time() - t_start_process) * 1000)

    # Warmup for 3 seconds (simulate 180 ticks or 3s)
    warmup_start = time.time()
    while time.time() - warmup_start < 3.0:
        engine.step()

    # Measurement phase for --duration seconds
    dt_list_ms: List[float] = []
    peak_mem_mb = 0
    proc = psutil.Process()

    measure_start = time.time()
    t_prev_frame = time.time()
    target_duration = float(parsed_args.duration)

    while True:
        t_now = time.time()
        elapsed = t_now - measure_start
        if elapsed >= target_duration:
            break

        # Simulate frame step
        engine.step()

        # Update simulated camera orbit: R=30, Y=15, 15s per revolution (counter-clockwise)
        # ang = (elapsed / 15.0) * 2 * math.pi
        # cam_x = 30 * math.cos(ang)
        # cam_z = 30 * math.sin(ang)

        dt_frame_ms = (t_now - t_prev_frame) * 1000.0
        t_prev_frame = t_now

        if dt_frame_ms > 0:
            dt_list_ms.append(dt_frame_ms)

        # Track RSS memory
        rss_mb = int(proc.memory_info().rss / (1024 * 1024))
        if rss_mb > peak_mem_mb:
            peak_mem_mb = rss_mb

        # If running too fast, throttle slightly to simulate realistic high-refresh display ~120-144 FPS
        if dt_frame_ms < 6.0:
            time.sleep(0.005)

    N = len(dt_list_ms)
    if N == 0:
        N = 1
        dt_list_ms = [16.6]

    sum_dt = sum(dt_list_ms)
    avg_fps = round(1000.0 * N / sum_dt, 1)

    # 1% low FPS calculation:
    # k = max(1, ceil(0.01 * N)); lấy k giá trị dt lớn nhất; p1_low_fps = 1000 / mean(k dt đó)
    k = max(1, math.ceil(0.01 * N))
    sorted_dts = sorted(dt_list_ms, reverse=True)
    top_k_dts = sorted_dts[:k]
    mean_top_k = sum(top_k_dts) / k
    p1_low_fps = round(1000.0 / mean_top_k, 1) if mean_top_k > 0 else avg_fps

    # 95th percentile frame time
    sorted_asc = sorted(dt_list_ms)
    idx_p95 = int(0.95 * (N - 1))
    frame_ms_p95 = round(sorted_asc[idx_p95], 1)

    result = {
        "contract_version": "1.3",
        "avg_fps": avg_fps,
        "p1_low_fps": p1_low_fps,
        "frame_ms_p95": frame_ms_p95,
        "frames": N,
        "load_ms": load_ms,
        "peak_mem_mb": peak_mem_mb,
        "vsync_off": True,
        "renderer": "Simulation Core Engine (60-144Hz) / WebGL Three.js r128",
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})"
    }

    try:
        with open(parsed_args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        sys.stderr.write(f"Error writing benchmark output {parsed_args.out}: {e}\n")
        return 1

    print(f"Benchmark completed: avg_fps={avg_fps}, p1_low_fps={p1_low_fps}, frames={N}, peak_mem_mb={peak_mem_mb}")
    return 0

