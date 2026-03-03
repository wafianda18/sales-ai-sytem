"""Prediction endpoint."""
from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import verify_token
from models.schemas import PredictRequest, PredictResponse
from services.ml_service import ml_service

router = APIRouter(prefix="/predict", tags=["ML Prediction"])


@router.post(
    "",
    response_model=PredictResponse,
    summary="Predict product sales status",
    description=(
        "Given product metrics, returns whether the product is predicted to be "
        "**Laris** (popular) or **Tidak** (not popular), along with confidence score."
    ),
)
def predict(body: PredictRequest, _user: dict = Depends(verify_token)):
    try:
        result = ml_service.predict(
            jumlah_penjualan=body.jumlah_penjualan,
            harga=body.harga,
            diskon=body.diskon,
        )
        return PredictResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
