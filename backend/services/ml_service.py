"""ML model loader and prediction service (singleton pattern)."""
import json
import numpy as np
import pandas as pd
import joblib
import os

from config import MODEL_PATH, SCALER_PATH, META_PATH


class MLService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        """Load model artifacts from disk (called once at startup)."""
        if self._loaded:
            return
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run ml/train.py first.")
        self.model  = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)
        with open(META_PATH) as f:
            self.meta = json.load(f)
        self._loaded = True
        print(f"[MLService] Model loaded. Test acc={self.meta.get('test_accuracy')}")

    def predict(self, jumlah_penjualan: float, harga: float, diskon: float) -> dict:
        """Build feature vector, scale, predict, return result dict."""
        if not self._loaded:
            self.load()

        # Mirror preprocessing in train.py
        revenue          = jumlah_penjualan * harga
        harga_after_disc = harga * (1 - diskon / 100)
        sales_per_price  = jumlah_penjualan / (harga + 1)

        features = pd.DataFrame([{
            "jumlah_penjualan": jumlah_penjualan,
            "harga":            harga,
            "diskon":           diskon,
            "revenue":          revenue,
            "harga_after_disc": harga_after_disc,
            "sales_per_price":  sales_per_price,
        }])

        features_scaled = self.scaler.transform(features)
        label_idx  = int(self.model.predict(features_scaled)[0])
        proba      = self.model.predict_proba(features_scaled)[0]
        confidence = float(proba[label_idx])

        # label_map stored as str keys in JSON → convert
        label_map  = {int(k): v for k, v in self.meta["label_map"].items()}
        status     = label_map[label_idx]

        return {
            "status":      status,
            "confidence":  round(confidence, 4),
            "label_index": label_idx,
            "features_used": {
                "jumlah_penjualan": jumlah_penjualan,
                "harga":            harga,
                "diskon":           diskon,
                "revenue":          revenue,
                "harga_after_disc": harga_after_disc,
                "sales_per_price":  round(sales_per_price, 6),
            },
        }


ml_service = MLService()
