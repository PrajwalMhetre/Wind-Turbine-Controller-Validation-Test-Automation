from windtest.runner import run_suite
from windtest.scenarios import SCENARIOS

def test_all_scenarios_pass():
    results = run_suite()
    assert len(results) == len(SCENARIOS)
    failures = {r.name: r.failures for r in results if not r.passed}
    assert not failures, failures

def test_unknown_scenario_is_rejected():
    import pytest
    with pytest.raises(ValueError, match="Unknown scenario"):
        run_suite(["not_a_real_scenario"])
