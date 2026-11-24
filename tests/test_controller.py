from windtest.config import ControllerConfig
from windtest.controller import WindTurbineController
from windtest.types import FaultCode, OperatingState, SensorSnapshot

def test_valid_start_enters_running_state():
    c = WindTurbineController()
    out = c.update(SensorSnapshot(8, 0, 25), start=True)
    assert out.state is OperatingState.RUNNING
    assert 0 < out.power_command_kw <= c.config.rated_power_kw
    assert not out.brake_applied

def test_emergency_stop_latches_safe_state():
    out = WindTurbineController().update(SensorSnapshot(8, 8, 25, emergency_stop=True))
    assert out.state is OperatingState.FAULT
    assert out.fault is FaultCode.EMERGENCY_STOP
    assert out.fault_latched and out.power_command_kw == 0 and out.brake_applied

def test_reset_rejected_while_trip_active():
    c = WindTurbineController()
    c.update(SensorSnapshot(26, 0, 25))
    out = c.update(SensorSnapshot(26, 0, 25), reset=True)
    assert out.fault_latched and out.state is OperatingState.FAULT

def test_reset_after_trip_clear_returns_stopped():
    c = WindTurbineController()
    c.update(SensorSnapshot(26, 0, 25))
    out = c.update(SensorSnapshot(8, 0, 25), reset=True)
    assert not out.fault_latched and out.state is OperatingState.STOPPED

def test_invalid_config_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        ControllerConfig(cut_in_wind_mps=15, rated_wind_mps=12)
