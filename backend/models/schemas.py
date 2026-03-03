"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List


# ── Auth ───────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserInfo"

class UserInfo(BaseModel):
    username: str
    full_name: str
    role: str

TokenResponse.model_rebuild()


# ── Sales ──────────────────────────────────────────────────────────────────────
class SalesItem(BaseModel):
    product_id:       str
    product_name:     str
    jumlah_penjualan: int
    harga:            float
    diskon:           float
    status:           str

class SalesResponse(BaseModel):
    total:  int
    data:   List[SalesItem]
    laris:  int
    tidak:  int


# ── Prediction ─────────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    jumlah_penjualan: float = Field(..., ge=0, example=350)
    harga:            float = Field(..., ge=0, example=750000)
    diskon:           float = Field(..., ge=0, le=100, example=10)

class PredictResponse(BaseModel):
    status:      str          # "Laris" | "Tidak"
    confidence:  float        # probability 0–1
    label_index: int
    features_used: dict


# ── Error ──────────────────────────────────────────────────────────────────────
class ErrorResponse(BaseModel):
    detail: str
