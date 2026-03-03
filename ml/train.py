"""
ML Training Script - Sales Status Classifier
Problem: Binary classification (Laris / Tidak)
Model: Random Forest Classifier
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)
import joblib
import json
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "../data/sales_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
SCALER_PATH= os.path.join(BASE_DIR, "scaler.joblib")
META_PATH  = os.path.join(BASE_DIR, "model_meta.json")

# ── 1. Load & Inspect ──────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[Data] Loaded {len(df)} rows, columns: {list(df.columns)}")
    print(df.head())
    print("\n[Data] Class distribution:")
    print(df["status"].value_counts())
    return df

# ── 2. Preprocessing ───────────────────────────────────────────────────────────
def preprocess(df: pd.DataFrame):
    features = ["jumlah_penjualan", "harga", "diskon"]
    target   = "status"

    X = df[features].copy()
    y = df[target].copy()

    # Encode target: Laris=1, Tidak=0
    le = LabelEncoder()
    y_enc = le.fit_transform(y)  # ['Laris','Tidak'] → [1, 0]
    label_map = {int(le.transform([c])[0]): c for c in le.classes_}

    # Feature engineering: revenue proxy & discount-adjusted price
    X["revenue"]          = X["jumlah_penjualan"] * X["harga"]
    X["harga_after_disc"] = X["harga"] * (1 - X["diskon"] / 100)
    X["sales_per_price"]  = X["jumlah_penjualan"] / (X["harga"] + 1)

    print(f"\n[Prep] Feature matrix shape: {X.shape}")
    print(X.describe())

    return X, y_enc, le, label_map

# ── 3. Train ───────────────────────────────────────────────────────────────────
def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_split=2,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train_sc, y_train)

    return model, scaler, X_train_sc, X_test_sc, y_train, y_test

# ── 4. Evaluate ────────────────────────────────────────────────────────────────
def evaluate(model, scaler, X, y, X_test_sc, y_test, label_map):
    y_pred = model.predict(X_test_sc)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n[Eval] Test Accuracy : {acc:.4f} ({acc*100:.2f}%)")

    # Cross-validation
    X_sc = scaler.transform(X)
    cv_scores = cross_val_score(model, X_sc, y, cv=5, scoring="accuracy")
    print(f"[Eval] CV Accuracy   : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Detailed report
    target_names = [label_map[0], label_map[1]]
    print("\n[Eval] Classification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    print("[Eval] Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature importance
    feature_names = X.columns.tolist()
    importances = model.feature_importances_
    fi = sorted(zip(feature_names, importances), key=lambda x: -x[1])
    print("\n[Eval] Feature Importances:")
    for name, imp in fi:
        print(f"  {name:<25}: {imp:.4f}")

    return {
        "test_accuracy": round(acc, 4),
        "cv_mean":       round(float(cv_scores.mean()), 4),
        "cv_std":        round(float(cv_scores.std()), 4),
        "feature_importances": {n: round(float(i), 4) for n, i in fi},
        "label_map": label_map,
    }

# ── 5. Save ────────────────────────────────────────────────────────────────────
def save_artifacts(model, scaler, meta: dict):
    joblib.dump(model,  MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"\n[Save] Model  → {MODEL_PATH}")
    print(f"[Save] Scaler → {SCALER_PATH}")
    print(f"[Save] Meta   → {META_PATH}")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df                            = load_data(DATA_PATH)
    X, y_enc, le, label_map       = preprocess(df)
    model, scaler, X_tr, X_te, y_tr, y_te = train(X, y_enc)
    meta                          = evaluate(model, scaler, X, y_enc, X_te, y_te, label_map)
    meta["features_used"]         = X.columns.tolist()
    save_artifacts(model, scaler, meta)
    print("\n✅ Training complete.")
