# agents_system/data_ingestor.py
import os
import datetime
from typing import Dict, Any, Tuple, Optional
from sentinelhub import (
    SHConfig,
    BBox,
    CRS,
    SentinelHubRequest,
    DataCollection,
    MimeType,
    bbox_to_dimensions,
)

# ======== CONFIGURATION ========
SH_CLIENT_ID = os.getenv("SENTINELHUB_CLIENT_ID")
SH_CLIENT_SECRET = os.getenv("SENTINELHUB_CLIENT_SECRET")
SH_BASE_URL = os.getenv("SENTINELHUB_BASE_URL", "https://services.sentinel-hub.com")
SH_TOKEN_URL = os.getenv("SENTINELHUB_OAUTH_TOKEN_URL", "https://oauth.sentinel-hub.com/oauth/token")

config = SHConfig()
config.sh_client_id = SH_CLIENT_ID
config.sh_client_secret = SH_CLIENT_SECRET
config.sh_base_url = SH_BASE_URL
config.sh_token_url = SH_TOKEN_URL

# ======== EVALSCRIPT (computes NDVI + vegetation mask) ========
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B04", "B08", "dataMask"] }],
    output: [
      { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
      { id: "mask", bands: 1, sampleType: "UINT8" }
    ]
  };
}

function evaluatePixel(sample) {
  var red = sample.B04;
  var nir = sample.B08;
  var ndvi = (nir - red) / (nir + red + 1e-6);
  var mask = ndvi >= 0.4 ? 1 : 0;
  return [ndvi, mask];
}
"""

# ======== HELPER FUNCTIONS ========

async def _make_request(bbox: Tuple[float, float, float, float], time_range: Tuple[str, str]):
    """Perform SentinelHub Process API request."""
    bb = BBox(bbox=bbox, crs=CRS.WGS84)
    size = bbox_to_dimensions(bb, resolution=10)
    request = SentinelHubRequest(
        evalscript=EVALSCRIPT,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=time_range,
            mosaicking_order='mostRecent',
        )],
        responses=[
            SentinelHubRequest.output_response('ndvi', MimeType.TIFF),
            SentinelHubRequest.output_response('mask', MimeType.TIFF),
        ],
        bbox=bb,
        size=size,
        config=config,
    )
    return request.get_data()

def compute_percent_and_mean(ndvi_array, mask_array):
    """Compute average NDVI and % vegetation pixels."""
    import numpy as np
    ndvi_vals = ndvi_array.astype(float)
    mask_vals = mask_array.astype(bool)
    mean_ndvi = float(np.nanmean(ndvi_vals))
    valid_pixels = ~np.isnan(ndvi_vals)
    pct = 100.0 * (mask_vals & valid_pixels).sum() / valid_pixels.sum()
    return mean_ndvi, pct

# ======== MAIN FUNCTION ========

async def fetch_forest_cover(region: str,
                             bbox: Optional[Tuple[float,float,float,float]] = None,
                             current_days: int = 10,
                             lag_days: int = 40,
                             window_days: int = 10) -> Dict[str, Any]:
    """
    Fetch forest cover metrics for `region`, comparing two time windows:
    - current window: last `current_days`
    - previous window: (`lag_days` - `lag_days` + `window_days`)
    """
    import numpy as np

    if not bbox:
        bbox = (90.0, 26.0, 91.0, 27.0)  # Default test bbox (Assam, India)

    today = datetime.date.today()
    # Current: last 10 days
    current_range = ((today - datetime.timedelta(days=current_days)).isoformat(), today.isoformat())
    # Previous: 40-30 days ago
    prev_end = today - datetime.timedelta(days=lag_days - window_days)
    prev_start = prev_end - datetime.timedelta(days=window_days)
    previous_range = (prev_start.isoformat(), prev_end.isoformat())

    # ---- Fetch current window ----
    data_curr = await _make_request(bbox, current_range)
    ndvi_array_curr, mask_array_curr = data_curr[0], data_curr[1]
    mean_ndvi_curr, forest_pct_curr = compute_percent_and_mean(ndvi_array_curr, mask_array_curr)

    # ---- Fetch previous window ----
    data_prev = await _make_request(bbox, previous_range)
    ndvi_array_prev, mask_array_prev = data_prev[0], data_prev[1]
    mean_ndvi_prev, forest_pct_prev = compute_percent_and_mean(ndvi_array_prev, mask_array_prev)

    # ---- Return both ----
    return {
        "region": region,
        "date": current_range[1],
        "forest_percent": round(forest_pct_curr, 2),
        "previous_forest_percent": round(forest_pct_prev, 2),
        "ndvi_mean": float(round(mean_ndvi_curr, 3)),
        "previous_ndvi_mean": float(round(mean_ndvi_prev, 3)),
        "source": "sentinelhub",
        "bbox": bbox,
        "current_range": current_range,
        "previous_range": previous_range,
    }
