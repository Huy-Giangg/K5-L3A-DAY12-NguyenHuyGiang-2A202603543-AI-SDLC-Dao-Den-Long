import argparse
import json
import sys
from typing import Dict, Any, List, Optional
from src.core.models import Tuning
from src.core.engine import SimulationEngine

def load_json_file(file_path: str) -> Any:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error reading JSON file {file_path}: {e}\n")
        sys.exit(2)

def run_headless(args_list: Optional[List[str]] = None) -> int:
    # If called with no arguments at all, output status OK for health checks
    if args_list is None:
        args_list = sys.argv[1:]
    if len(args_list) == 0:
        print("STATUS: OK - Headless mode running successfully.")
        return 0

    parser = argparse.ArgumentParser(description="Dao Den Long Headless Runner (Contract v1.0)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--night", type=int, default=1, help="Night level (default: 1)")
    parser.add_argument("--scenario", type=str, default=None, help="Scenario json file path")
    parser.add_argument("--inputs", type=str, default=None, help="Inputs json file path")
    parser.add_argument("--ticks", type=int, required=True, help="Number of ticks to simulate")
    parser.add_argument("--out", type=str, required=True, help="Output jsonl file path")
    parser.add_argument("--snapshot-every", type=int, default=10, help="Snapshot interval (default: 10)")

    try:
        parsed_args = parser.parse_args(args_list)
    except SystemExit as e:
        return 2 if e.code != 0 else 0

    # Parse scenario
    scenario_data = None
    if parsed_args.scenario:
        scenario_data = load_json_file(parsed_args.scenario)
        if not isinstance(scenario_data, dict):
            sys.stderr.write("Scenario JSON must be an object\n")
            sys.exit(2)

    # Parse inputs
    input_frames_by_tick: Dict[int, Dict[str, Any]] = {}
    if parsed_args.inputs:
        inputs_data = load_json_file(parsed_args.inputs)
        if not isinstance(inputs_data, dict) or "frames" not in inputs_data or not isinstance(inputs_data["frames"], list):
            sys.stderr.write("Inputs JSON must be an object with a 'frames' list\n")
            sys.exit(2)
        
        last_tick = -1
        for frame in inputs_data["frames"]:
            if not isinstance(frame, dict) or "tick" not in frame:
                sys.stderr.write("Each frame in inputs must be an object with 'tick'\n")
                sys.exit(2)
            f_tick = frame["tick"]
            if f_tick <= last_tick:
                sys.stderr.write("Input frame ticks must be strictly increasing\n")
                sys.exit(2)
            last_tick = f_tick
            input_frames_by_tick[f_tick] = frame

    # Load tuning from game.contract.json if present
    tuning = Tuning()
    try:
        with open("game.contract.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            if "tuning" in c_data:
                t = c_data["tuning"]
                for k, v in t.items():
                    if hasattr(tuning, k) and v is not None:
                        setattr(tuning, k, v)
                if "score" in t and isinstance(t["score"], dict):
                    sc = t["score"]
                    tuning.per_mote_score = sc.get("per_mote", tuning.per_mote_score)
                    tuning.per_lantern_score = sc.get("per_lantern", tuning.per_lantern_score)
                    tuning.per_stun_score = sc.get("per_stun", tuning.per_stun_score)
                    tuning.per_second_left_score = sc.get("per_second_left", tuning.per_second_left_score)
                    tuning.per_flame_left_score = sc.get("per_flame_left", tuning.per_flame_left_score)
    except Exception:
        pass # fallback to default Tuning

    engine = SimulationEngine(seed=parsed_args.seed, tuning=tuning)
    if scenario_data:
        engine.apply_scenario(scenario_data)

    out_lines: List[str] = []

    # Snapshot at tick 0
    snap0 = engine.get_snapshot()
    out_lines.append(json.dumps(snap0, separators=(',', ':')))

    total_ticks = parsed_args.ticks
    snap_interval = parsed_args.snapshot_every

    for k in range(total_ticks):
        if engine.state != "playing":
            break

        # Check if input exists for tick k
        if k in input_frames_by_tick:
            engine.apply_input_frame(input_frames_by_tick[k])

        engine.step()

        # Emit events occurring in step k -> recorded at tick k+1
        for event in engine.events_this_tick:
            out_lines.append(json.dumps(event, separators=(',', ':')))

        # Emit snapshot if on interval
        if engine.tick % snap_interval == 0:
            out_lines.append(json.dumps(engine.get_snapshot(), separators=(',', ':')))

    # End record
    out_lines.append(json.dumps(engine.get_end_record(), separators=(',', ':')))

    try:
        with open(parsed_args.out, "w", encoding="utf-8") as f:
            for line in out_lines:
                f.write(line + "\n")
    except Exception as e:
        sys.stderr.write(f"Error writing output to {parsed_args.out}: {e}\n")
        return 1

    return 0
