# Software Requirement-to-Test Traceability

These are project-level software requirements for this simulated example, not OEM requirements or standards-derived requirements.

| ID | Requirement | Verification |
|---|---|---|
| SW-CTRL-001 | Start accepted only inside configured wind window | test_valid_start_enters_running_state; startup_and_run |
| SW-CTRL-002 | Stop request inhibits commanded generation | controlled_stop |
| SW-PROT-001 | Emergency stop latches fault and safe outputs | test_emergency_stop_latches_safe_state; emergency_stop |
| SW-PROT-002 | Rotor overspeed trips | test_overspeed_trip_has_safe_outputs; overspeed |
| SW-PROT-003 | Cut-out wind trips | high_wind_shutdown |
| SW-PROT-004 | Invalid/non-finite sensor data trips | test_nan_sensor_value_trips_sensor_fault; sensor_failure |
| SW-PROT-005 | Grid loss inhibits generation | test_grid_loss_is_latched; grid_loss |
| SW-PROT-006 | Reset blocked until trip condition clears | test_reset_rejected_while_trip_active; fault_reset_interlock |
| SW-LIM-001 | Power command remains within configured bounds | test_all_scenarios_pass; runner invariants |
| SW-CFG-001 | Invalid wind thresholds rejected | test_invalid_config_is_rejected |

For real development, link each ID to controlled system/software requirements, hazard controls, interface specifications, test procedures, and approved evidence.
