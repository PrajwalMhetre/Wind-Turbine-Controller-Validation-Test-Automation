# API Reference

- `ControllerConfig`: immutable configuration dataclass with validation of wind, rotor, temperature and power limits.
- `SensorSnapshot`: sensor input values (m/s, rpm, °C), grid availability, emergency-stop status and sensor validity.
- `WindTurbineController.update(snapshot, start=False, stop=False, reset=False)`: updates the state machine and returns a ControllerOutput. Protection faults latch; reset is accepted only when modelled trip conditions clear.
- `run_scenario(scenario, config=None)`: executes one deterministic scenario and returns observations, checks and failures.
- `run_suite(names=None, config=None)`: executes all or selected scenarios; unknown names raise ValueError.
- `windtest list`: print scenario names.
- `windtest run`: run the complete suite.
- `windtest run --scenario overspeed --output reports/overspeed.json`: run one test and save a JSON report.
