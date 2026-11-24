# Hardware and HIL Integration

## Safety boundary
There is no fieldbus driver or hardware command path in this repository. Do not connect this code to production turbines or use it to actuate pitch, brakes, contactors, converters, or grid interfaces. Hardware integration is a separate safety-engineered activity.

## Adapter concept
Keep scenario and assertion logic independent of the transport. A future bench adapter may expose operations conceptually equivalent to:
- `read_sensors() -> SensorSnapshot`
- `write_supervisory_request(start, stop, reset)`
- `read_outputs() -> ControllerOutput`
- `close()`

The current test runner operates on an in-process reference controller. A future HIL runner must use a separately reviewed interface implementation, starting in read-only mode.

## Required controls before HIL
1. Approved interface-control document: signals, units, scaling, endian, update rates, validity bits and timeouts.
2. Hazard analysis and safe-state definition reviewed by responsible functional-safety engineers.
3. Electrical isolation, current limits, independent emergency stop and safe bench fixture.
4. Watchdog, communication-loss handling, stale-data detection and bounded command rates.
5. HIL procedure with calibrated instruments, tolerances, preconditions and abort criteria.
6. Access control, change review, complete event logging and independent verification.
7. OEM/site approvals before any field connection.

Industrial interfaces could include CAN/CANopen, Modbus, EtherCAT or vendor-specific protocols. Select only from the actual controller's approved interface specification.

## Evidence
Capture firmware/build, hardware revision, adapter version, calibration status, procedure revision, test environment, operator, raw traces, timestamps and deviations. A simulator JSON report is not HIL evidence.
