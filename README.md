# Canary Deployment API with FastAPI

![Architecture](image.png)


## 🔁 Canary Deployment Flow (Step-by-step)

1. **Startup:**
   - `main.py` loads the **stable model** (`model_v1.joblib`).
   - All predictions use this model by default.

2. **Deploy Canary:**
   - Use the endpoint `/admin/deploy-canary` to load `model_v2.joblib` into memory.
   - After deployment, **10% of predictions** are randomly routed to the canary.

3. **Generate Traffic:**
   - Send prediction requests via `/predict`.
   - Use `curl.py` or manual `curl` commands to simulate traffic.

4. **Simulate Slowdown (Optional):**
   - Use `/admin/toggle-slowdown` to introduce artificial delay in the canary model.

5. **Check Health:**
   - Call `/admin/check-canary-health`.
   - The server compares latencies using **Welch's t-test**.
   - If the canary is significantly slower, an alert is triggered.

6. **Promote or Rollback:**
   - If performance is acceptable, call `/admin/promote-canary`.
   - If degraded, call `/admin/rollback-canary`.


---


## 📁 Project Structure


```
canary_project/
├── app/
│   ├── routes.py          # All FastAPI endpoints (predict, deploy, rollback, etc.)
│   └── state.py           # Global state: models, metrics, flags
├── models/
│   ├── model_v1.joblib    # Stable model (Logistic Regression)
│   └── model_v2.joblib    # Canary model (Logistic Regression with noise)
├── train.py               # Trains and saves both v1 and v2 models
├── main.py                # Starts FastAPI app and loads initial state
├── curl.py                # Simulates traffic and executes full canary testing flow
├── requirements.txt       # Required Python packages
└── README.md              # Project description and instructions
```



---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/audrey-siqueira/canary_project.git
   cd canary_project

2. Install required packages:
   ```bash
   pip install -r requirements.txt


## 🚀 Running the Project
  
3. Train models
    ```bash
   python train.py
    
4. Start the API
   ```bash
   #The API will be live at: http://0.0.0.0:8000
   python main.py

## 🔁 Canary Testing Flow

5. You can use the included curl.py to simulate the full lifecycle:
   ```bash
   python curl.py

   #This script will:
   
   #1) Deploy the canary model (/admin/deploy-canary)
   
   #2) Send 300 inference requests (/predict)
   
   #3) Perform statistical health check (/admin/check-canary-health)
   
   #4) Toggle slowdown (/admin/toggle-slowdown) - ARTIFICIAL DELAY
   
   #5) Send more traffic
   
   #6) Perform another health check
   
   #7) Roll back the canary if needed
   
   #8) Confirm rollback with a new prediction
