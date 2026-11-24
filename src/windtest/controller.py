"""Deterministic supervisory state machine for software verification only."""
from __future__ import annotations
import math
from .config import ControllerConfig
from .types import ControllerOutput, FaultCode, OperatingState, SensorSnapshot

class WindTurbineController:
    """Simplified reference controller; not production turbine-control software."""

    def __init__(self, config: ControllerConfig | None = None) -> None:
        self.config = config or ControllerConfig()
        self.output = ControllerOutput()

    def update(self, sensors: SensorSnapshot, *, start: bool = False,
               stop: bool = False, reset: bool = False) -> ControllerOutput:
        cfg = self.config
        if self.output.fault_latched:
            if reset and self._trip_cleared(sensors):
                self.output = ControllerOutput(message="Fault reset; turbine remains stopped")
            else:
                self._safe_fault_output()
                return self.output

        fault = self._detect_fault(sensors)
        if fault is not FaultCode.NONE:
            self.output.fault = fault
            self.output.fault_latched = True
            self.output.message = f"Latched protection trip: {fault.value}"
            self._safe_fault_output()
            return self.output

        if stop:
            self.output.state = OperatingState.SHUTTING_DOWN
            self.output.power_command_kw = 0.0
            self.output.pitch_command_deg = cfg.shutdown_pitch_deg
            self.output.brake_applied = True
            self.output.message = "Controlled stop requested"
            return self.output

        if self.output.state in (OperatingState.STOPPED, OperatingState.SHUTTING_DOWN):
            if start and cfg.cut_in_wind_mps <= sensors.wind_speed_mps < cfg.cut_out_wind_mps:
                self.output.state = OperatingState.STARTING
                self.output.brake_applied = False
                self.output.pitch_command_deg = cfg.operating_pitch_deg
                self.output.message = "Startup conditions accepted"
            else:
                self.output.state = OperatingState.STOPPED
                self.output.power_command_kw = 0.0
                self.output.brake_applied = True
                self.output.pitch_command_deg = cfg.shutdown_pitch_deg
                self.output.message = "Waiting for valid start request"
                return self.output

        if self.output.state is OperatingState.STARTING:
            self.output.state = OperatingState.RUNNING
            self.output.message = "Startup complete"

        if sensors.wind_speed_mps < cfg.cut_in_wind_mps:
            self.output.state = OperatingState.SHUTTING_DOWN
            self.output.power_command_kw = 0.0
            self.output.pitch_command_deg = cfg.shutdown_pitch_deg
            self.output.brake_applied = True
            self.output.message = "Below cut-in wind; shutdown"
        elif not sensors.grid_available:
            # Grid loss is detected as a latched protection fault by _detect_fault.
            self._safe_fault_output()
        elif sensors.wind_speed_mps < cfg.rated_wind_mps:
            self.output.state = OperatingState.RUNNING
            fraction = (sensors.wind_speed_mps - cfg.cut_in_wind_mps) / (
                cfg.rated_wind_mps - cfg.cut_in_wind_mps
            )
            self.output.power_command_kw = max(0.0, min(cfg.rated_power_kw, fraction * cfg.rated_power_kw))
            self.output.pitch_command_deg = cfg.operating_pitch_deg
            self.output.brake_applied = False
        else:
            self.output.state = OperatingState.DERATED
            self.output.power_command_kw = cfg.rated_power_kw
            self.output.pitch_command_deg = cfg.derated_pitch_deg
            self.output.brake_applied = False
        return self.output

    def _detect_fault(self, sensors: SensorSnapshot) -> FaultCode:
        cfg = self.config
        if sensors.emergency_stop:
            return FaultCode.EMERGENCY_STOP
        values = (sensors.wind_speed_mps, sensors.rotor_speed_rpm,
                  sensors.generator_temperature_c)
        if not sensors.sensor_valid or not all(math.isfinite(v) for v in values):
            return FaultCode.SENSOR_INVALID
        if sensors.rotor_speed_rpm > cfg.rated_rotor_speed_rpm * cfg.overspeed_trip_ratio:
            return FaultCode.OVERSPEED
        if sensors.wind_speed_mps >= cfg.cut_out_wind_mps:
            return FaultCode.HIGH_WIND
        if sensors.generator_temperature_c >= cfg.max_generator_temperature_c:
            return FaultCode.GENERATOR_OVERTEMP
        if not sensors.grid_available:
            return FaultCode.GRID_LOSS
        return FaultCode.NONE

    def _trip_cleared(self, sensors: SensorSnapshot) -> bool:
        values = (sensors.wind_speed_mps, sensors.rotor_speed_rpm,
                  sensors.generator_temperature_c)
        return (
            sensors.sensor_valid and all(math.isfinite(v) for v in values)
            and not sensors.emergency_stop
            and sensors.rotor_speed_rpm <= self.config.rated_rotor_speed_rpm
            and sensors.wind_speed_mps < self.config.cut_out_wind_mps
            and sensors.generator_temperature_c < self.config.max_generator_temperature_c
            and sensors.grid_available
        )

    def _safe_fault_output(self) -> None:
        self.output.state = OperatingState.FAULT
        self.output.power_command_kw = 0.0
        self.output.pitch_command_deg = self.config.shutdown_pitch_deg
        self.output.brake_applied = True
