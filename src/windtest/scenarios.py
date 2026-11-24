"""Reusable deterministic scenario definitions."""
from dataclasses import dataclass
from .types import SensorSnapshot

@dataclass(frozen=True)
class ScenarioStep:
    label: str
    sensors: SensorSnapshot
    start: bool = False
    stop: bool = False
    reset: bool = False
    expected_state: str | None = None
    expected_fault: str | None = None
    expected_power_zero: bool = False

@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    steps: tuple[ScenarioStep, ...]

def S(wind: float, rpm: float = 0.0, temp: float = 25.0, **kwargs) -> SensorSnapshot:
    return SensorSnapshot(wind, rpm, temp, **kwargs)

SCENARIOS: dict[str, Scenario] = {
    "startup_and_run": Scenario("startup_and_run", "Start in valid wind and enter generation.", (
        ScenarioStep("start", S(8), start=True, expected_state="running"),
        ScenarioStep("steady", S(9, 10), expected_state="running"))),
    "rated_wind": Scenario("rated_wind", "Operate at rated wind.", (
        ScenarioStep("rated", S(12), start=True, expected_state="derated"),)),
    "high_wind_shutdown": Scenario("high_wind_shutdown", "Cut-out wind trips protection.", (
        ScenarioStep("high-wind", S(26), expected_fault="high_wind", expected_power_zero=True),)),
    "overspeed": Scenario("overspeed", "Rotor overspeed trips protection.", (
        ScenarioStep("overspeed", S(10, 19), expected_fault="overspeed", expected_power_zero=True),)),
    "emergency_stop": Scenario("emergency_stop", "Emergency stop latches safe state.", (
        ScenarioStep("e-stop", S(8, 8, emergency_stop=True),
                     expected_fault="emergency_stop", expected_power_zero=True),)),
    "sensor_failure": Scenario("sensor_failure", "Invalid sensor data causes a latched trip.", (
        ScenarioStep("invalid-sensor", S(8, sensor_valid=False),
                     expected_fault="sensor_invalid", expected_power_zero=True),)),
    "grid_loss": Scenario("grid_loss", "Grid loss inhibits generation through a trip.", (
        ScenarioStep("grid-loss", S(8, 8, grid_available=False),
                     expected_fault="grid_loss", expected_power_zero=True),)),
    "controlled_stop": Scenario("controlled_stop", "A stop request commands zero power.", (
        ScenarioStep("start", S(8), start=True, expected_state="running"),
        ScenarioStep("stop", S(8, 8), stop=True, expected_state="shutting_down",
                     expected_power_zero=True))),
    "fault_reset_interlock": Scenario("fault_reset_interlock", "Reset only after trip clearance.", (
        ScenarioStep("trip", S(26), expected_fault="high_wind", expected_power_zero=True),
        ScenarioStep("reset-active", S(26), reset=True, expected_fault="high_wind",
                     expected_power_zero=True),
        ScenarioStep("clear-reset", S(8), reset=True, expected_state="stopped"))),
}
