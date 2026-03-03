"""Application configuration."""
import os

SECRET_KEY    = os.getenv("SECRET_KEY", "supersecret-jwt-key-change-in-prod")
ALGORITHM     = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Dummy users (in production: use a database)
DUMMY_USERS = {
    "admin": {
        "username": "admin",
        "password": "admin123",   # plain-text for demo; hash in prod
        "full_name": "Admin User",
        "role": "admin",
    },
    "analyst": {
        "username": "analyst",
        "password": "analyst123",
        "full_name": "Sales Analyst",
        "role": "viewer",
    },
}

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH   = os.path.join(BASE_DIR, "data", "sales_data.csv")
MODEL_PATH  = os.path.join(BASE_DIR, "ml", "model.joblib")
SCALER_PATH = os.path.join(BASE_DIR, "ml", "scaler.joblib")
META_PATH   = os.path.join(BASE_DIR, "ml", "model_meta.json")
