"""Versioned JSON report serialization."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from .types import ScenarioResult

def report_dict(results: Iterable[ScenarioResult]) -> dict:
    items = list(results)
    passed = sum(item.passed for item in items)
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {"total": len(items), "passed": passed, "failed": len(items) - passed,
                    "success_rate_percent": round(100 * passed / len(items), 2) if items else 100.0},
        "scenarios": [{
            "name": item.name, "description": item.description, "passed": item.passed,
            "failures": item.failures,
            "observations": [{"step": obs.step, "wind_speed_mps": obs.wind_speed_mps,
                "rotor_speed_rpm": obs.rotor_speed_rpm, "output": obs.output,
                "checks": obs.checks} for obs in item.observations],
            "metadata": item.metadata,
        } for item in items],
    }

def write_json_report(results: Iterable[ScenarioResult], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report_dict(results), indent=2), encoding="utf-8")
    return target
