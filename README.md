# Wind Turbine Controller Validation & Test Automation

A Python-based controller verification playground for wind-turbine supervisory and protection logic. It combines a deterministic plant/controller simulator, reusable test scenarios, safety-invariant checks, structured result reporting, and continuous integration.

> **Scope and safety:** This is an educational/software verification framework. The included plant and controller are simplified simulations, not an OEM model, safety PLC, certified protection system, or substitute for commissioning procedures. Never connect experimental code directly to a live turbine. Real hardware use requires an independently engineered interface, risk assessment, validated limits, isolation, and qualified review.

## Features

- Deterministic simulated turbine with operating states, rotor speed, wind speed, generator power, pitch, and fault inputs.
- Controller state machine with startup, normal operation, derating, shutdown, and fault lockout.
- Configurable operating limits and safety-invariant checks.
- Scenarios for startup, rated operation, high wind, overspeed, emergency stop, sensor faults, grid loss, and reset interlocks.
- Pytest unit/integration tests and machine-readable JSON reports.
- CLI for running all scenarios or a selected scenario.
- GitHub Actions CI across Python 3.10–3.12.
- Engineering documentation: architecture, test strategy, scenario catalogue, traceability, API, and hardware integration guidance.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
windtest run --output reports/latest.json
```

Run a single scenario and list available scenarios:

```bash
windtest run --scenario emergency_stop --output reports/emergency_stop.json
windtest list
```

## Project layout

```text
src/windtest/       # controller, plant, scenarios, runner, CLI, reports
tests/              # unit, scenario, and safety-invariant tests
docs/               # architecture, validation plan, traceability, integration
.github/workflows/  # CI pipeline
```

## Operating assumptions

Illustrative defaults: cut-in wind 3 m/s, rated wind 12 m/s, cut-out wind 25 m/s, rotor overspeed threshold 1.2 per-unit of rated speed. These are configurable software-test values, **not design recommendations**. Actual settings must come from the turbine manufacturer and site-specific engineering basis.

## Safety behaviour modelled

- Stop command requests controlled shutdown.
- Emergency stop and critical faults latch a fault state.
- Overspeed, high wind, over-temperature, grid loss, and invalid sensor values trigger protection.
- Reset is rejected while a trip condition remains active.
- Latched fault commands zero power, shutdown pitch, and brake applied.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Validation test plan](docs/TEST_PLAN.md)
- [Scenario catalogue](docs/SCENARIOS.md)
- [Requirements-to-test traceability](docs/TRACEABILITY.md)
- [Hardware/HIL integration](docs/HARDWARE_INTEGRATION.md)
- [API reference](docs/API.md)
- [Contributing](docs/CONTRIBUTING.md)

The simulator report is regression evidence only; it is not a certification record or demonstration of physical stopping performance.

## License

MIT. See [LICENSE](LICENSE).
