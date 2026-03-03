// src/components/StatsCards.jsx
export default function StatsCards({ stats }) {
  const cards = [
    { label: "Total Products",  value: stats.total,           icon: "📦", cls: "stat-total"  },
    { label: "Laris",           value: stats.laris,           icon: "🚀", cls: "stat-laris"  },
    { label: "Tidak Laris",     value: stats.tidak,           icon: "📉", cls: "stat-tidak"  },
    {
      label: "Laris Rate",
      value: stats.total ? `${((stats.laris / stats.total) * 100).toFixed(1)}%` : "0%",
      icon: "📈",
      cls: "stat-rate",
    },
  ];

  return (
    <div className="stats-grid">
      {cards.map(c => (
        <div key={c.label} className={`stat-card ${c.cls}`}>
          <div className="stat-icon">{c.icon}</div>
          <div className="stat-value">{c.value}</div>
          <div className="stat-label">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
