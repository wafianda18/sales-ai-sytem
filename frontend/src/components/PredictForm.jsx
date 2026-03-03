// src/components/PredictForm.jsx
import { useState } from "react";
import { predict } from "../services/api";

const fmtIDR = (n) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(n);

export default function PredictForm() {
  const [form, setForm] = useState({ jumlah_penjualan: "", harga: "", diskon: "" });
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const handleChange = (e) =>
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setResult(null); setLoading(true);
    try {
      const data = await predict(
        parseFloat(form.jumlah_penjualan),
        parseFloat(form.harga),
        parseFloat(form.diskon),
      );
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isLaris = result?.status === "Laris";

  return (
    <div className="predict-layout">
      <div className="card predict-form-card">
        <div className="card-header"><h3>🤖 Predict Sales Status</h3></div>
        <p className="predict-desc">
          Enter product metrics to get an AI-powered prediction on whether
          the product will be <strong>Laris</strong> (popular) or <strong>Tidak Laris</strong>.
        </p>

        <form onSubmit={handleSubmit} className="predict-form">
          <div className="form-group">
            <label>Jumlah Penjualan (units)</label>
            <input
              type="number" name="jumlah_penjualan"
              value={form.jumlah_penjualan}
              onChange={handleChange}
              placeholder="e.g. 350" min="0" required
            />
            <span className="form-hint">Total units sold</span>
          </div>

          <div className="form-group">
            <label>Harga (IDR)</label>
            <input
              type="number" name="harga"
              value={form.harga}
              onChange={handleChange}
              placeholder="e.g. 750000" min="0" required
            />
            <span className="form-hint">Unit price in Rupiah</span>
          </div>

          <div className="form-group">
            <label>Diskon (%)</label>
            <input
              type="number" name="diskon"
              value={form.diskon}
              onChange={handleChange}
              placeholder="e.g. 10" min="0" max="100" required
            />
            <span className="form-hint">Discount percentage (0–100)</span>
          </div>

          {error && <div className="error-msg">⚠ {error}</div>}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Analyzing…" : "🔮 Predict"}
          </button>
        </form>
      </div>

      {result && (
        <div className={`card result-card ${isLaris ? "result-laris" : "result-tidak"}`}>
          <div className="result-icon">{isLaris ? "🚀" : "📉"}</div>
          <div className="result-label">Prediction Result</div>
          <div className={`result-status ${isLaris ? "text-laris" : "text-tidak"}`}>
            {isLaris ? "LARIS" : "TIDAK LARIS"}
          </div>

          <div className="confidence-bar-wrap">
            <div className="confidence-label">
              Confidence: <strong>{(result.confidence * 100).toFixed(1)}%</strong>
            </div>
            <div className="confidence-bar">
              <div
                className={`confidence-fill ${isLaris ? "fill-laris" : "fill-tidak"}`}
                style={{ width: `${result.confidence * 100}%` }}
              />
            </div>
          </div>

          <div className="result-features">
            <h4>Feature Breakdown</h4>
            {Object.entries(result.features_used).map(([k, v]) => (
              <div key={k} className="feature-row">
                <span className="feature-key">{k}</span>
                <span className="feature-val">
                  {k === "harga" || k === "harga_after_disc"
                    ? fmtIDR(v)
                    : k === "revenue"
                    ? fmtIDR(v)
                    : typeof v === "number" && v > 100
                    ? v.toLocaleString("id-ID")
                    : v}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
