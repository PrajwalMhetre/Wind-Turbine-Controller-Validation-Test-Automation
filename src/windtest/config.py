"""Illustrative test limits; use approved turbine-specific data for real systems."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ControllerConfig:
    cut_in_wind_mps: float = 3.0
    rated_wind_mps: float = 12.0
    cut_out_wind_mps: float = 25.0
    rated_rotor_speed_rpm: float = 15.0
    overspeed_trip_ratio: float = 1.20
    max_generator_temperature_c: float = 105.0
    rated_power_kw: float = 2000.0
    shutdown_pitch_deg: float = 90.0
    operating_pitch_deg: float = 5.0
    derated_pitch_deg: float = 20.0

    def __post_init__(self) -> None:
        if not (0 < self.cut_in_wind_mps < self.rated_wind_mps < self.cut_out_wind_mps):
            raise ValueError("Wind thresholds must satisfy 0 < cut-in < rated < cut-out")
        if self.rated_rotor_speed_rpm <= 0 or self.overspeed_trip_ratio <= 1:
            raise ValueError("Rotor speed must be positive and overspeed ratio greater than 1")
        if self.rated_power_kw <= 0 or self.max_generator_temperature_c <= 0:
            raise ValueError("Power and temperature limits must be positive")
