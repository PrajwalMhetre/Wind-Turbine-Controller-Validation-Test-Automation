# Scenario Catalogue

| Scenario | Stimulus | Expected outcome |
|---|---|---|
| startup_and_run | Start at 8 m/s, then steady operation | RUNNING and bounded power |
| rated_wind | Wind at 12 m/s rated threshold | DERATED |
| high_wind_shutdown | Wind at/above cut-out | Latched high-wind trip, zero power |
| overspeed | Rotor above configured threshold | Latched overspeed trip |
| emergency_stop | Emergency-stop asserted | Latched emergency trip |
| sensor_failure | Sensor-valid flag false | Sensor fault and safe outputs |
| grid_loss | Grid unavailable | Latched grid-loss trip |
| controlled_stop | Start then stop | SHUTTING_DOWN and zero power |
| fault_reset_interlock | Trip; reset while active; clear and reset | Reset blocked until clear |

## Adding a scenario
1. Add a uniquely named Scenario in `src/windtest/scenarios.py`.
2. Define deterministic SensorSnapshot stimuli.
3. Declare expected state, fault and output conditions.
4. Add pytest coverage for safety-relevant behaviour.
5. Run pytest and the CLI; inspect the JSON report.
6. Update this catalogue and the traceability matrix.
