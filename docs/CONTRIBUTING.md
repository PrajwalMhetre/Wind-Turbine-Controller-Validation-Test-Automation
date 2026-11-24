# Contributing

1. Create a feature branch.
2. Keep physical units explicit in names and documentation.
3. Add deterministic tests for every new behaviour.
4. Avoid hidden global state, sleeps and nondeterministic stimuli.
5. Preserve the hardware safety boundary: no live control path in this repository.
6. Run `ruff check .` and `pytest` before submitting.
7. Update scenario documentation and traceability for added requirements.
8. State assumptions, limitations and supporting evidence in pull requests.

Use Python 3.10+, type hints, dataclasses for domain data, and pytest for automated verification. JSON output is regression evidence, not certification evidence.
