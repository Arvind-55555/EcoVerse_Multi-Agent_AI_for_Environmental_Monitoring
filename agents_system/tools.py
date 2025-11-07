# Lightweight wrappers for function tools that agents can call
from agents import function_tool


@function_tool
def create_ticket(title: str, description: str, priority: str = "medium") -> dict:
"""Create a ticket (placeholder). Replace with Jira/ServiceNow API calls."""
# In production: call Jira / database / ticketing API
return {"ticket_id": "GM-0001", "title": title, "status": "created", "priority": priority}


@function_tool
def post_slack(message: str) -> dict:
"""Post a message to Slack via webhook. This is synchronous; for higher throughput use async requests."""
import requests
from ..config import settings
if not settings.slack_webhook_url:
return {"ok": False, "error": "no webhook configured"}
res = requests.post(settings.slack_webhook_url, json={"text": message})
return {"ok": res.ok, "status_code": res.status_code}