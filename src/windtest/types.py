"""Shared domain types."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

class OperatingState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    DERATED = "derated"
    SHUTTING_DOWN = "shutting_down"
    FAULT = "fault"

class FaultCode(str, Enum):
    NONE = "none"
    EMERGENCY_STOP = "emergency_stop"
    OVERSPEED = "overspeed"
    HIGH_WIND = "high_wind"
    SENSOR_INVALID = "sensor_invalid"
    GENERATOR_OVERTEMP = "generator_overtemp"
    GRID_LOSS = "grid_loss"

@dataclass(frozen=True)
class SensorSnapshot:
    wind_speed_mps: float
    rotor_speed_rpm: float
    generator_temperature_c: float
    grid_available: bool = True
    emergency_stop: bool = False
    sensor_valid: bool = True

@dataclass
class ControllerOutput:
    state: OperatingState = OperatingState.STOPPED
    power_command_kw: float = 0.0
    pitch_command_deg: float = 90.0
    brake_applied: bool = True
    fault: FaultCode = FaultCode.NONE
    fault_latched: bool = False
    message: str = "Initialised"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["state"] = self.state.value
        result["fault"] = self.fault.value
        return result

@dataclass
class StepObservation:
    step: int
    wind_speed_mps: float
    rotor_speed_rpm: float
    output: dict[str, Any]
    checks: dict[str, bool] = field(default_factory=dict)

@dataclass
class ScenarioResult:
    name: str
    description: str
    passed: bool
    observations: list[StepObservation]
    failures: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)
