from typing import Dict, Any


async def make_report(metrics: Dict[str, Any], analysis: Dict[str, Any], plan: Dict[str, Any], execution: Dict[str, Any]) -> str:
lines = []
lines.append(f"Region: {metrics.get('region')}")
lines.append(f"Date: {metrics.get('date')}")
lines.append("\n=== Analysis ===")
lines.append(str(analysis))
lines.append("\n=== Plan ===")
lines.append(str(plan))
lines.append("\n=== Execution ===")
lines.append(str(execution))
return "\n".join(lines)