# Running the Turbine Simulation

The simulator is a deterministic, closed-loop software model. It feeds simulated sensor measurements to the reference controller, applies controller outputs to the simplified plant model, and records the time series.

## Run

```bash
windtest simulate
windtest simulate --duration 300 --dt 0.5 --wind 10
windtest simulate --duration 180 --dt 1 --wind 14 --output reports/high-wind-run.json
```

Arguments:
- `--duration`: simulation horizon in seconds (default 120).
- `--dt`: fixed integration step in seconds (default 1).
- `--wind`: constant wind input in m/s (default 8).
- `--output`: JSON output path.

The report includes time, wind speed, rotor speed, generator temperature, controller state, power command, pitch command, brake state, and fault code for every sample.

## Model limitations

The plant uses a simple first-order rotor-speed response and illustrative thermal behaviour. Wind is constant during a run. It does not model aerodynamic torque, blade element dynamics, drivetrain torsion, converter controls, pitch actuator dynamics, turbulence, wake effects, grid transients, or real-time execution. It is suitable for demonstrating software test automation, not engineering design or turbine performance prediction.
