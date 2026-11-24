# Validation Test Plan

## Objective
Verify state transitions, protection-trip latching, reset interlocks, command bounds, and deterministic regression behaviour in the simulated controller.

## Verification levels
| Level | Target | Method |
|---|---|---|
| Unit | Configuration and controller transitions | pytest |
| Scenario | Multi-step functional sequences | Scenario runner |
| Invariant | Safe-output and command-bound properties | Assertions per step |
| Regression | Full scenario catalogue | GitHub Actions |
| HIL (future) | Bench-controller interface and timing | Separately approved procedure |

## Entry criteria
- Python 3.10+ and development dependencies installed.
- Test limits reviewed as illustrative values, not deployed values.

## Exit criteria
- All automated tests pass.
- Every scenario yields a verdict.
- No configured software invariant is violated.
- JSON report is retained as test evidence.

## Current invariants
- Power command is non-negative and no greater than rated power.
- FAULT commands zero power and shutdown pitch.
- A latched fault keeps brake applied.

These software-model properties do not prove physical stopping distance, actuator response, SIL/PL, grid-code compliance, or certification. The model has no real-time scheduler, electrical sensor fault injection, fieldbus driver, or validated aeroelastic/generator dynamics.
