"""Scenario executor and safety-invariant verdicts."""
from .config import ControllerConfig
from .controller import WindTurbineController
from .scenarios import SCENARIOS, Scenario
from .types import ScenarioResult, StepObservation

def run_scenario(scenario: Scenario, config: ControllerConfig | None = None) -> ScenarioResult:
    controller = WindTurbineController(config)
    observations: list[StepObservation] = []
    failures: list[str] = []
    for index, step in enumerate(scenario.steps, start=1):
        output = controller.update(step.sensors, start=step.start, stop=step.stop, reset=step.reset)
        checks = {
            "power_non_negative": output.power_command_kw >= 0.0,
            "power_within_rated_limit": output.power_command_kw <= controller.config.rated_power_kw,
            "fault_state_zero_power": output.state.value != "fault" or output.power_command_kw == 0.0,
            "fault_state_shutdown_pitch": output.state.value != "fault" or
                output.pitch_command_deg == controller.config.shutdown_pitch_deg,
            "latched_fault_brake_applied": not output.fault_latched or output.brake_applied,
        }
        if step.expected_state and output.state.value != step.expected_state:
            failures.append(f"step {index} ({step.label}): expected state {step.expected_state}, got {output.state.value}")
        if step.expected_fault and output.fault.value != step.expected_fault:
            failures.append(f"step {index} ({step.label}): expected fault {step.expected_fault}, got {output.fault.value}")
        if step.expected_power_zero and output.power_command_kw != 0.0:
            failures.append(f"step {index} ({step.label}): expected zero power, got {output.power_command_kw}")
        for name, passed in checks.items():
            if not passed:
                failures.append(f"step {index} ({step.label}): invariant failed: {name}")
        observations.append(StepObservation(index, step.sensors.wind_speed_mps,
            step.sensors.rotor_speed_rpm, output.to_dict(), checks))
    return ScenarioResult(scenario.name, scenario.description, not failures,
                          observations, failures)

def run_suite(names: list[str] | None = None, config: ControllerConfig | None = None):
    selected = names if names is not None else list(SCENARIOS)
    unknown = sorted(set(selected) - set(SCENARIOS))
    if unknown:
        raise ValueError(f"Unknown scenario(s): {', '.join(unknown)}")
    return [run_scenario(SCENARIOS[name], config) for name in selected]
