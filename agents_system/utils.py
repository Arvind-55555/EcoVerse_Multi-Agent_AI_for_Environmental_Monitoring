import json


def summarize_changes(change_metrics: dict) -> str:
return json.dumps(change_metrics, indent=2)