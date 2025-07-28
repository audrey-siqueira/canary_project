# Canary Deployment API with FastAPI

This project demonstrates a simplified **Canary Deployment** architecture using **FastAPI** for model serving, latency monitoring, and statistical validation via Welch's t-test. A stable model (`model_v1`) is deployed by default, and a canary model (`model_v2`) can be deployed and evaluated in production before promotion.

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
