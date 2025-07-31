# app/routes.py
import random
import time
from fastapi import FastAPI
from pydantic import BaseModel
from scipy.stats import ttest_ind
from pathlib import Path
from datetime import datetime
from typing import Optional
from joblib import load
from fastapi import Query
from statsmodels.stats.power import TTestIndPower

from .state import ( stable_model, 
                     stable_model_path,
                     canary_model, 
                     canary_model_path,
                     canary_start_time, 
                     metrics,
                     alert_status, 
                     simulate_slowdown 
)

app = FastAPI()

class InputData(BaseModel):
    features: list[float]




@app.post("/predict")
async def predict(data: InputData):
    global simulate_slowdown, canary_model

    use_canary = random.random() < 0.1 and canary_model is not None
    model_name = "canary" if use_canary else "stable"
    model = canary_model if use_canary else stable_model

    start = time.perf_counter()
    if simulate_slowdown and use_canary:
        time.sleep(0.01)
    proba = model.predict_proba([data.features])[0][1]
    latency_ms = (time.perf_counter() - start) * 1000

    metrics[model_name]["latencies_ms"].append(latency_ms)

    return {
        "churn_probability": proba,
        "model_used": model_name,
        "latency_ms": latency_ms
    }

@app.post("/admin/deploy-canary")
async def deploy_canary(payload: dict):
    global canary_model, canary_model_path, canary_start_time

    path = payload.get("model_path")
    if not path or not Path(path).exists():
        return {"status": "error", "message": f"Model file not found: {path}"}

    try:
        canary_model = load(path)
        canary_model_path = path
        canary_start_time = datetime.utcnow()
        metrics["canary"] = {"latencies_ms": []}

        return {
            "status": "success",
            "message": "Canary model deployed successfully",
            "model_path": path,
            "canary_start_time": canary_start_time.isoformat()
        }
    except Exception:
        return {"status": "error", "message": f"Model file not found: {path}"}




@app.post("/admin/rollback-canary")
async def rollback_canary():
    global canary_model, canary_model_path, canary_start_time

    if canary_model is None:
        return {"status": "error", "message": "No active canary to rollback"}

    canary_model = None
    canary_model_path = None
    canary_start_time = None
    metrics["canary"] = {"latencies_ms": []}

    alert_status.update({"alert": False, "p_value": None, "v1_avg_latency": None, "v2_avg_latency": None})

    return {"status": "success", "message": "Canary rolled back successfully"}







@app.get("/admin/check-canary-health")
async def check_canary_health():
    if canary_model is None:
        return {"alert_triggered": False, "message": "No active canary deployment to monitor."}

    stable = metrics["stable"]["latencies_ms"]
    canary = metrics["canary"]["latencies_ms"]
    if len(stable) < 20 or len(canary) < 20:
        return { "alert_triggered": False,
                 "message": "Insufficient data for statistical analysis. Need at least 20 samples for both models.",
                 "stable_sample_count": len(stable),
                 "canary_sample_count": len(canary) }

    stat, pvalue = ttest_ind(canary, stable, equal_var=False)
    v1_avg = sum(stable) / len(stable)
    v2_avg = sum(canary) / len(canary)
    alert = (pvalue < 0.05) and (v2_avg > v1_avg)

    alert_status.update({ "alert": alert,
                          "p_value": pvalue,
                          "v1_avg_latency": v1_avg,
                          "v2_avg_latency": v2_avg })

    if alert:
        return { "alert_triggered": True,
                 "p_value": pvalue,
                 "message": "ALERT: Canary latency is significantly higher than stable.",
                 "stable_avg_latency_ms": v1_avg,
                 "canary_avg_latency_ms": v2_avg,
                 "stable_sample_count": len(stable),
                 "canary_sample_count": len(canary)
            }
    else:
        return { "alert_triggered": False,
                 "p_value": pvalue,
                 "message": "Canary performance is acceptable.",
                 "stable_avg_latency_ms": v1_avg,
                 "canary_avg_latency_ms": v2_avg,
                 "stable_sample_count": len(stable),
                 "canary_sample_count": len(canary) }



@app.post("/admin/promote-canary")
async def promote_canary():
    global stable_model, stable_model_path
    global canary_model, canary_model_path, canary_start_time

    if canary_model is None:
        return {"status": "error", "message": "No active canary to promote"}

    previous_stable_path = stable_model_path

    stable_model = canary_model
    stable_model_path = canary_model_path

    canary_model = None
    canary_model_path = None
    canary_start_time = None
    metrics["canary"] = {"latencies_ms": []}

    alert_status.update({"alert": False, "p_value": None, "v1_avg_latency": None, "v2_avg_latency": None})

    return { "status": "success",
             "message": "Canary promoted to stable successfully",
             "previous_stable_model": previous_stable_path,
             "new_stable_model": stable_model_path}




@app.post("/admin/toggle-slowdown")
async def toggle_slowdown():
    global simulate_slowdown
    simulate_slowdown = not simulate_slowdown
    return { "simulate_slowdown": simulate_slowdown,
             "message": "Slowdown simulation " + ("enabled" if simulate_slowdown else "disabled")}




@app.get("/admin/power-analysis")
async def power_analysis(
    effect_size: float = Query(0.666, description="Effect size (delta / std)"),
    alpha: float = Query(0.05, description="Significance level"),
    power: float = Query(0.8, description="Power of the test")
):
    analysis = TTestIndPower()
    sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, ratio=1.0)
    return {
        "effect_size": effect_size,
        "alpha": alpha,
        "power": power,
        "recommended_sample_size_per_group": int(sample_size)
    }
