# ⚡ Mini AI Sales Prediction System

> Sistem prediksi penjualan berbasis Machine Learning dengan REST API dan dashboard React.

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐      HTTP/JWT       ┌──────────────────────┐      predict()       ┌─────────────────┐
│   FRONTEND      │ ◄──────────────────►│     BACKEND          │ ◄─────────────────►  │   ML MODULE     │
│  React + Vite   │                     │  FastAPI + Python    │                      │  scikit-learn   │
│  localhost:5173 │                     │  localhost:8000      │                      │  RandomForest   │
└─────────────────┘                     └──────────┬───────────┘                      └────────┬────────┘
                                                   │ pandas.read_csv                           │ train/load
                                                   ▼                                           ▼
                                              ┌─────────────────────────────────────────────────────┐
                                              │              DATA LAYER: sales_data.csv             │
                                              └─────────────────────────────────────────────────────┘
```

### Alur Data
1. **Login** — Frontend POST `/auth/login` → Backend validasi dummy user → JWT dikirim balik
2. **Sales Data** — Frontend GET `/sales` (dengan Bearer JWT) → Backend baca CSV dengan Pandas → JSON response
3. **Prediksi** — Frontend POST `/predict` (dengan input jumlah/harga/diskon) → Backend panggil ML Service → Model RandomForest predict → JSON response

---

## 📁 Struktur Project

```
sales-ai-sytem/
├── backend/
│   ├── main.py               # FastAPI app, CORS, startup
│   ├── config.py             # Settings, paths, dummy users
│   ├── requirements.txt
│   ├── routers/
│   │   ├── auth.py           # POST /auth/login
│   │   ├── sales.py          # GET  /sales
│   │   └── predict.py        # POST /predict
│   ├── models/
│   │   └── schemas.py        # Pydantic request/response models
│   ├── services/
│   │   └── ml_service.py     # Singleton: load model, predict
│   └── middleware/
│       └── auth.py           # JWT create / verify
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── context/AuthContext.jsx
│   │   ├── services/api.js
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   └── DashboardPage.jsx
│   │   └── components/
│   │       ├── SalesTable.jsx
│   │       ├── PredictForm.jsx
│   │       └── StatsCards.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── ml/
│   ├── train.py              # Training script
│   ├── model.joblib          # Trained model (after running train.py)
│   ├── scaler.joblib         # Feature scaler
│   └── model_meta.json       # Accuracy, feature importances
├── data/
│   └── sales_data.csv
├── architecture.svg
└── README.md
```

---

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Jalankan ML Training

```bash
cd project-root
pip install scikit-learn pandas numpy joblib

python ml/train.py
# Output: model.joblib, scaler.joblib, model_meta.json
# Test Accuracy: 90.00%  |  CV: 98.00% ± 4.00%
```

### 2. Jalankan Backend

```bash
cd backend
pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

- API Base: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs ← interactive API explorer
- Health check: http://localhost:8000/health

### 3. Jalankan Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173

### 4. Login

| Username | Password    | Role    |
|----------|-------------|---------|
| admin    | admin123    | admin   |
| analyst  | analyst123  | viewer  |

---

## 🤖 Machine Learning

### Model: Random Forest Classifier

**Problem**: Binary classification — prediksi apakah produk "Laris" atau "Tidak"

**Input features (raw)**:
- `jumlah_penjualan` — total unit terjual
- `harga` — harga satuan (IDR)
- `diskon` — diskon dalam persen

**Engineered features**:
- `revenue = jumlah_penjualan × harga`
- `harga_after_disc = harga × (1 - diskon/100)`
- `sales_per_price = jumlah_penjualan / harga` (volume vs price ratio)

**Evaluasi**:
| Metric         | Value  |
|----------------|--------|
| Test Accuracy  | 90.00% |
| CV Accuracy    | 98.00% |
| CV Std Dev     | ±4.00% |

**Feature Importance** (top):
1. `jumlah_penjualan` — 53.6%
2. `sales_per_price`  — 13.7%
3. `revenue`          — 12.7%

---

## 🔌 API Reference

### `POST /auth/login`
```json
// Request
{ "username": "admin", "password": "admin123" }

// Response 200
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": { "username": "admin", "full_name": "Admin User", "role": "admin" }
}
```

### `GET /sales?status=Laris`
*Header: `Authorization: Bearer <token>`*
```json
{
  "total": 27,
  "laris": 27,
  "tidak": 23,
  "data": [{ "product_id": "P001", "product_name": "...", "jumlah_penjualan": 320, ... }]
}
```

### `POST /predict`
*Header: `Authorization: Bearer <token>`*
```json
// Request
{ "jumlah_penjualan": 350, "harga": 750000, "diskon": 10 }

// Response 200
{
  "status": "Laris",
  "confidence": 0.87,
  "label_index": 1,
  "features_used": { "jumlah_penjualan": 350, "harga": 750000, ... }
}
```

---

## 🧠 Design Decisions

### Backend
- **FastAPI** dipilih karena auto-generates OpenAPI/Swagger docs, async support, Pydantic validation out of the box
- **Singleton pattern** untuk `MLService` — model hanya di-load sekali saat startup, tidak tiap request
- **Pydantic schemas** dipisahkan di `models/schemas.py` untuk clean separation of concerns
- **JWT dengan python-jose** — stateless auth, cocok untuk SPA
- Error handling menggunakan HTTPException dengan status code yang tepat (401, 422, 503)

### Machine Learning
- **Random Forest** dipilih karena robust terhadap outliers, tidak butuh feature scaling yang ketat, dan memberikan feature importance
- **Feature engineering** (revenue, harga_after_disc, sales_per_price) menambah signal untuk model
- **StandardScaler** diterapkan sebelum training dan disimpan untuk dipakai ulang saat inference — menghindari data leakage
- **class_weight="balanced"** untuk handle class imbalance ringan (27 Laris vs 23 Tidak)
- Model disimpan dengan **joblib** (lebih efisien dari pickle untuk numpy arrays)

### Frontend
- **Vite** sebagai bundler untuk development experience yang cepat
- **Context API** untuk auth state — cukup untuk skala app ini, tidak perlu Redux
- **localStorage** untuk persist JWT token antar refresh
- Vite **proxy** ke backend menghindari CORS issue saat development

---

## ⚠️ Asumsi

1. **Dummy authentication** — user disimpan di memori (dict), bukan database. Di production: gunakan database + bcrypt hashing
2. **CSV sebagai data source** — data dibaca dari file setiap request GET /sales. Di production: gunakan database (PostgreSQL/SQLite)
3. **Dataset kecil (50 rows)** — model dilatih dengan data yang dibuat secara representatif. Akurasi tinggi (98% CV) karena pola cukup jelas
4. **Label "Laris" = jumlah_penjualan tinggi** — asumsi ini tercermin di feature importance (jumlah_penjualan = 53.6%)
5. **Single-user deployment** — tidak ada multi-tenancy atau rate limiting
6. **Secret key hardcoded** — dalam production, harus di-load dari environment variable / secret manager
