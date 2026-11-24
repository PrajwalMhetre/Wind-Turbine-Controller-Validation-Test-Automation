"""Simplified deterministic plant model for tests; not a validated digital twin."""
from dataclasses import dataclass
from .config import ControllerConfig
from .types import ControllerOutput, SensorSnapshot

@dataclass
class SimulatedTurbine:
    config: ControllerConfig
    wind_speed_mps: float = 0.0
    rotor_speed_rpm: float = 0.0
    generator_temperature_c: float = 25.0
    grid_available: bool = True
    emergency_stop: bool = False
    sensor_valid: bool = True

    def step(self, output: ControllerOutput, dt_seconds: float = 1.0) -> None:
        if dt_seconds <= 0:
            raise ValueError("dt_seconds must be positive")
        target = 0.0 if output.brake_applied else min(
            self.config.rated_rotor_speed_rpm,
            self.wind_speed_mps / self.config.rated_wind_mps * self.config.rated_rotor_speed_rpm,
        )
        alpha = min(1.0, dt_seconds / 5.0)
        self.rotor_speed_rpm += alpha * (target - self.rotor_speed_rpm)
        heat = output.power_command_kw / self.config.rated_power_kw * 0.04
        cooling = max(0.0, self.generator_temperature_c - 25.0) * 0.001
        self.generator_temperature_c += dt_seconds * (heat - cooling)

    def sensors(self) -> SensorSnapshot:
        return SensorSnapshot(self.wind_speed_mps, self.rotor_speed_rpm,
                              self.generator_temperature_c, self.grid_available,
                              self.emergency_stop, self.sensor_valid)
