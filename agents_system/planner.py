from typing import Dict, Any


async def build_plan(analysis: Dict[str, Any], region: str) -> Dict[str, Any]:
"""Create a short mitigation/action plan.
Returns steps and estimated effort.
"""
steps = []
if analysis.get("is_anomaly"):
steps.append({"step": "Validate with higher-res imagery", "eta": "2 days"})
steps.append({"step": "Notify local forestry team", "eta": "1 day"})
steps.append({"step": "Create ground survey ticket", "eta": "3 days"})
effort = "medium"
else:
steps.append({"step": "Keep monitoring", "eta": "7 days"})
effort = "low"
return {"region": region, "steps": steps, "effort": effort}