# No need to call fetch twice — the ingestor now provides both.
async def detect_anomaly(metrics, threshold_pct=5.0):
    cur = metrics.get("forest_percent")
    prev = metrics.get("previous_forest_percent")
    if not prev or not cur:
        return {"is_anomaly": False, "reason": "missing previous data"}
    pct_change = ((cur - prev) / prev) * 100.0
    return {"is_anomaly": abs(pct_change) >= threshold_pct, "percent_change": pct_change}