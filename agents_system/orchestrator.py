import asyncio
from .data_ingestor import fetch_forest_cover
from .analyzer import detect_anomaly
from .planner import build_plan
from .executor import execute_actions
from .reporter import make_report
from .config import settings


async def run_for_region(region: str = "default-region"):
# 1) Fetch
metrics = await fetch_forest_cover(region)


# 2) Analyze
analysis = await detect_anomaly(metrics, threshold_pct=5.0)


# 3) Plan
plan = await build_plan(analysis, region)


# 4) Execute
execution = await execute_actions(plan)


# 5) Report
report = await make_report(metrics, analysis, plan, execution)


return {"metrics": metrics, "analysis": analysis, "plan": plan, "execution": execution, "report": report}


if __name__ == '__main__':
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--region', default='test-region')
args = parser.parse_args()
out = asyncio.run(run_for_region(args.region))
print(out['report'])