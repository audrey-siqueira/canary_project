from sklearn.linear_model import LogisticRegression
import numpy as np
from joblib import dump

# Stable Model - v1
X_v1 = np.random.rand(500, 5)
y_v1 = np.random.randint(0, 2, 500)
model_v1 = LogisticRegression().fit(X_v1, y_v1)
dump(model_v1, "models/model_v1.joblib")

# Canary Model - v2 (with noise)
X_v2 = X_v1 + np.random.normal(0, 0.01, X_v1.shape)
y_v2 = y_v1
model_v2 = LogisticRegression().fit(X_v2, y_v2)
dump(model_v2, "models/model_v2.joblib")

print("✅ Models trained and saved to 'models/' folder.")
