// src/pages/DashboardPage.jsx
import { useState, useEffect, useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import { getSales, predict } from "../services/api";
import SalesTable from "../components/SalesTable";
import PredictForm from "../components/PredictForm";
import StatsCards from "../components/StatsCards";

export default function DashboardPage() {
  const { user, signOut } = useAuth();
  const [sales, setSales]         = useState([]);
  const [stats, setStats]         = useState({ laris: 0, tidak: 0, total: 0 });
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState("");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [filter, setFilter]       = useState("");

  const fetchSales = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getSales(filter || undefined);
      setSales(data.data);
      setStats({ laris: data.laris, tidak: data.tidak, total: data.total });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { fetchSales(); }, [fetchSales]);

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span>⚡</span>
          <span>SalesAI</span>
        </div>
        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeTab === "dashboard" ? "active" : ""}`}
            onClick={() => setActiveTab("dashboard")}
          >
            <span className="nav-icon">📊</span> Dashboard
          </button>
          <button
            className={`nav-item ${activeTab === "predict" ? "active" : ""}`}
            onClick={() => setActiveTab("predict")}
          >
            <span className="nav-icon">🤖</span> Predict
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">{user?.username?.[0]?.toUpperCase()}</div>
            <div>
              <div className="user-name">{user?.full_name}</div>
              <div className="user-role">{user?.role}</div>
            </div>
          </div>
          <button className="btn-logout" onClick={signOut}>Sign Out</button>
        </div>
      </aside>

      {/* Main content */}
      <main className="main-content">
        <header className="page-header">
          <div>
            <h2>{activeTab === "dashboard" ? "Sales Dashboard" : "AI Prediction"}</h2>
            <p className="page-subtitle">
              {activeTab === "dashboard"
                ? "Overview of product sales performance"
                : "Predict whether a product will be popular"}
            </p>
          </div>
        </header>

        {activeTab === "dashboard" && (
          <>
            <StatsCards stats={stats} />

            <div className="card">
              <div className="card-header">
                <h3>Sales Data</h3>
                <div className="filter-group">
                  <label>Filter:</label>
                  <select value={filter} onChange={e => setFilter(e.target.value)}>
                    <option value="">All</option>
                    <option value="Laris">Laris</option>
                    <option value="Tidak">Tidak Laris</option>
                  </select>
                  <button className="btn-refresh" onClick={fetchSales}>↻ Refresh</button>
                </div>
              </div>

              {error && <div className="error-msg">⚠ {error}</div>}
              {loading
                ? <div className="loading-state">Loading data…</div>
                : <SalesTable data={sales} />
              }
            </div>
          </>
        )}

        {activeTab === "predict" && <PredictForm />}
      </main>
    </div>
  );
}
