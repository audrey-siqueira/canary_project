from joblib import load
from typing import Optional
from datetime import datetime

stable_model_path = "models/model_v1.joblib"
stable_model = load(stable_model_path)

canary_model_path: Optional[str] = None
canary_model = None
canary_start_time: Optional[datetime] = None

metrics = {
    "stable": {"latencies_ms": []},
    "canary": {"latencies_ms": []}
}

alert_status = {
    "alert": False,
    "p_value": None,
    "v1_avg_latency": None,
    "v2_avg_latency": None
}

simulate_slowdown = False