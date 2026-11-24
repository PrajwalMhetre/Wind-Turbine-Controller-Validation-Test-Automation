"""Closed-loop time-domain simulation using the simplified plant and controller."""
from __future__ import annotations
from dataclasses import asdict
import json
from pathlib import Path
from .config import ControllerConfig
from .controller import WindTurbineController
from .plant import SimulatedTurbine

def run_simulation(duration_s: float = 120.0, dt_s: float = 1.0,
                   wind_speed_mps: float = 8.0, output_path: str = "reports/simulation.json") -> dict:
    if duration_s <= 0 or dt_s <= 0 or wind_speed_mps < 0:
        raise ValueError("duration and dt must be positive; wind speed cannot be negative")
    cfg = ControllerConfig()
    controller = WindTurbineController(cfg)
    plant = SimulatedTurbine(config=cfg, wind_speed_mps=wind_speed_mps)
    samples = []
    steps = int(duration_s / dt_s)
    for index in range(steps + 1):
        sensors = plant.sensors()
        command = controller.update(sensors, start=(index == 0))
        samples.append({
            "time_s": round(index * dt_s, 3),
            "wind_speed_mps": plant.wind_speed_mps,
            "rotor_speed_rpm": plant.rotor_speed_rpm,
            "generator_temperature_c": plant.generator_temperature_c,
            "state": command.state.value,
            "power_command_kw": command.power_command_kw,
            "pitch_command_deg": command.pitch_command_deg,
            "brake_applied": command.brake_applied,
            "fault": command.fault.value,
        })
        if index < steps:
            plant.step(command, dt_s)
    result = {
        "simulation_type": "simplified_deterministic_closed_loop",
        "scope_warning": "Educational software model only; not an OEM digital twin or hardware validation.",
        "parameters": {"duration_s": duration_s, "dt_s": dt_s, "wind_speed_mps": wind_speed_mps},
        "summary": {
            "sample_count": len(samples),
            "final_state": samples[-1]["state"],
            "final_rotor_speed_rpm": samples[-1]["rotor_speed_rpm"],
            "final_power_command_kw": samples[-1]["power_command_kw"],
            "maximum_rotor_speed_rpm": max(s["rotor_speed_rpm"] for s in samples),
        },
        "samples": samples,
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    result["report_path"] = str(path)
    return result
