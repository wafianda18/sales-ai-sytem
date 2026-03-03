"""
Mini AI Sales Prediction System – FastAPI Backend
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
import sys
import os

# Ensure backend package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, sales, predict
from services.ml_service import ml_service

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Mini AI Sales Prediction API",
    description="""
## Mini AI Sales Prediction System

A REST API for managing sales data and predicting product popularity
using a **Random Forest** classifier trained on historical sales.

### Authentication
All protected endpoints require a **Bearer JWT** token.

1. Call `POST /auth/login` with valid credentials.
2. Copy the `access_token` from the response.
3. Click **Authorize** above and paste: `<token>` (without Bearer prefix in Swagger).

### Demo Credentials
| Username | Password    | Role    |
|----------|-------------|---------|
| admin    | admin123    | admin   |
| analyst  | analyst123  | viewer  |
    """,
    version="1.0.0",
    contact={"name": "Dev Team"},
    license_info={"name": "MIT"},
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup: preload ML model ─────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    try:
        ml_service.load()
    except FileNotFoundError as e:
        print(f"[WARNING] {e} – run ml/train.py first.")

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(predict.router)


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="API health check")
def root():
    return {
        "status": "ok",
        "message": "Mini AI Sales Prediction API",
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"], summary="Detailed health")
def health():
    return {
        "api": "ok",
        "ml_model_loaded": ml_service._loaded,
    }
