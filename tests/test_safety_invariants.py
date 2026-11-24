import math
from windtest.controller import WindTurbineController
from windtest.types import FaultCode, OperatingState, SensorSnapshot

def test_nan_sensor_value_trips_sensor_fault():
    out = WindTurbineController().update(SensorSnapshot(math.nan, 0, 25))
    assert out.fault is FaultCode.SENSOR_INVALID
    assert out.state is OperatingState.FAULT
    assert out.power_command_kw == 0 and out.brake_applied

def test_overspeed_trip_has_safe_outputs():
    c = WindTurbineController()
    out = c.update(SensorSnapshot(9, 19, 25))
    assert out.fault is FaultCode.OVERSPEED
    assert out.power_command_kw == 0
    assert out.pitch_command_deg == c.config.shutdown_pitch_deg

def test_grid_loss_is_latched():
    out = WindTurbineController().update(SensorSnapshot(9, 8, 25, grid_available=False))
    assert out.fault is FaultCode.GRID_LOSS and out.fault_latched
    assert out.power_command_kw == 0
