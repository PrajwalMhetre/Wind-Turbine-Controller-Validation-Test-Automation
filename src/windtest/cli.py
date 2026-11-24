"""Command-line entry point."""
import argparse
import sys
from .reporting import write_json_report
from .runner import run_suite
from .scenarios import SCENARIOS
from .simulation import run_simulation

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="windtest", description="Wind turbine controller validation runner")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List test scenarios")
    run = sub.add_parser("run", help="Execute scenario suite")
    run.add_argument("--scenario", action="append", help="Scenario name; can be repeated")
    run.add_argument("--output", default="reports/latest.json", help="JSON report destination")
    sim = sub.add_parser("simulate", help="Run closed-loop simulated turbine")
    sim.add_argument("--duration", type=float, default=120.0, help="Duration in seconds")
    sim.add_argument("--dt", type=float, default=1.0, help="Simulation time step in seconds")
    sim.add_argument("--wind", type=float, default=8.0, help="Constant wind speed in m/s")
    sim.add_argument("--output", default="reports/simulation.json", help="Simulation JSON report")
    return parser

def main() -> int:
    args = build_parser().parse_args()
    if args.command == "list":
        for name, scenario in SCENARIOS.items():
            print(f"{name:24} {scenario.description}")
        return 0
    if args.command == "simulate":
        result = run_simulation(args.duration, args.dt, args.wind, args.output)
        print("SIMULATION COMPLETE")
        print(f"Samples: {result['summary']['sample_count']}")
        print(f"Final state: {result['summary']['final_state']}")
        print(f"Final rotor speed: {result['summary']['final_rotor_speed_rpm']:.2f} rpm")
        print(f"Final power command: {result['summary']['final_power_command_kw']:.2f} kW")
        print(f"Report: {result['report_path']}")
        return 0
    results = run_suite(args.scenario)
    path = write_json_report(results, args.output)
    for result in results:
        print(f"{'PASS' if result.passed else 'FAIL'}  {result.name}")
        for failure in result.failures:
            print(f"      - {failure}")
    failures = sum(not item.passed for item in results)
    print(f"\n{len(results) - failures}/{len(results)} scenarios passed. Report: {path}")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
