"""Sales data endpoints."""
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, status

from config import DATA_PATH
from middleware.auth import verify_token
from models.schemas import SalesResponse, SalesItem

router = APIRouter(prefix="/sales", tags=["Sales Data"])


def _load_csv() -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sales data file not found.",
        )


@router.get(
    "",
    response_model=SalesResponse,
    summary="Get all sales data",
    description="Returns the full sales dataset. Requires Bearer JWT.",
)
def get_sales(
    status_filter: str | None = Query(None, alias="status", description="Filter by 'Laris' or 'Tidak'"),
    _user: dict = Depends(verify_token),
):
    df = _load_csv()

    if status_filter:
        df = df[df["status"].str.lower() == status_filter.lower()]

    items = [
        SalesItem(
            product_id=row["product_id"],
            product_name=row["product_name"],
            jumlah_penjualan=int(row["jumlah_penjualan"]),
            harga=float(row["harga"]),
            diskon=float(row["diskon"]),
            status=row["status"],
        )
        for _, row in df.iterrows()
    ]

    full_df = _load_csv()
    return SalesResponse(
        total=len(items),
        data=items,
        laris=int((full_df["status"] == "Laris").sum()),
        tidak=int((full_df["status"] == "Tidak").sum()),
    )
