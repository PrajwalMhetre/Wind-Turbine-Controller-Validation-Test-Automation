"""Command-line entry point."""
import argparse
import sys
from .reporting import write_json_report
from .runner import run_suite
from .scenarios import SCENARIOS

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="windtest", description="Wind turbine controller validation runner")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List test scenarios")
    run = sub.add_parser("run", help="Execute scenario suite")
    run.add_argument("--scenario", action="append", help="Scenario name; can be repeated")
    run.add_argument("--output", default="reports/latest.json", help="JSON report destination")
    return parser

def main() -> int:
    args = build_parser().parse_args()
    if args.command == "list":
        for name, scenario in SCENARIOS.items():
            print(f"{name:24} {scenario.description}")
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
