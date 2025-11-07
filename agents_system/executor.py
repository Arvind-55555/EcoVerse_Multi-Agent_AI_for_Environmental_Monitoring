from typing import Dict, Any
from .tools import create_ticket, post_slack


async def execute_actions(plan: Dict[str, Any]) -> Dict[str, Any]:
"""Execute the top action via function tool (ticket creation) and notify Slack."""
top_step = plan.get("steps", [])[0]
title = f"Action: {top_step['step']}"
description = f"Auto-generated action for region {plan.get('region')} — plan: {plan}"
ticket = create_ticket(title=title, description=description)
slack_resp = post_slack(f"Created ticket {ticket['ticket_id']} for region {plan.get('region')}")
return {"ticket": ticket, "slack": slack_resp}