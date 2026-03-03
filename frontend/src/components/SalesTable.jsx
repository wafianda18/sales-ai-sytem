// src/components/SalesTable.jsx
const fmt = (n) => new Intl.NumberFormat("id-ID").format(n);
const fmtIDR = (n) =>
  new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(n);

export default function SalesTable({ data }) {
  if (!data?.length) return <p className="empty-state">No data found.</p>;

  return (
    <div className="table-wrapper">
      <table className="sales-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Product Name</th>
            <th>Sales Qty</th>
            <th>Price</th>
            <th>Discount</th>
            <th>Revenue</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.product_id}>
              <td className="mono">{row.product_id}</td>
              <td>{row.product_name}</td>
              <td className="num">{fmt(row.jumlah_penjualan)}</td>
              <td className="num">{fmtIDR(row.harga)}</td>
              <td className="num">{row.diskon}%</td>
              <td className="num">{fmtIDR(row.jumlah_penjualan * row.harga * (1 - row.diskon / 100))}</td>
              <td>
                <span className={`badge ${row.status === "Laris" ? "badge-laris" : "badge-tidak"}`}>
                  {row.status === "Laris" ? "🚀 Laris" : "📉 Tidak"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
