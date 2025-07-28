# canary_project

# Canary Deployment API with FastAPI

This project demonstrates a simplified **Canary Deployment** architecture using **FastAPI** for model serving, latency monitoring, and statistical validation via Welch's t-test. A stable model (`model_v1`) is deployed by default, and a canary model (`model_v2`) can be deployed and evaluated in production before promotion.

---


## 📁 Project Structure

canary_project/
├── app/
│ ├── routes.py # All FastAPI endpoints (predict, deploy, rollback, etc.)
│ └── state.py # Global variables and application state (models, metrics, flags)
├── models/
│ ├── model_v1.joblib # Stable model (Logistic Regression)
│ └── model_v2.joblib # Canary model (Logistic Regression with noise)
├── train.py # Trains and saves both v1 and v2 models
├── main.py # Starts FastAPI app and loads initial state
├── curl.py # Simulates traffic and executes full canary testing flow
├── requirements.txt # Required Python packages
└── README.md # Project description and instructions



---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/audrey-siqueira/canary_project.git
   cd canary_project

2. Install required packages:
   ```bash
   pip install -r requirements.txt
