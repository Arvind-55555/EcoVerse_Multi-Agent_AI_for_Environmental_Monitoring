# Placeholder for test_agents.py
import asyncio
from agents_system.orchestrator import run_for_region


def test_run_smoke():
res = asyncio.run(run_for_region('unit-test-region'))
assert 'metrics' in res
assert 'analysis' in res
assert 'plan' in res
assert 'execution' in res
assert 'report' in