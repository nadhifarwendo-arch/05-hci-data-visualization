"""User-centered interactive dashboard demo for synthetic infrastructure assets."""
from pathlib import Path
import subprocess
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

st.set_page_config(page_title="Dashboard Aset Infrastruktur", page_icon="📊", layout="wide")


def load_data():
    assets_path = DATA / "assets.csv"
    events_path = DATA / "maintenance_events.csv"
    if not assets_path.exists() or not events_path.exists():
        subprocess.run([sys.executable, str(ROOT / "generate_data.py")], check=True)
    assets = pd.read_csv(assets_path, parse_dates=["installation_date", "last_inspection"])
    events = pd.read_csv(events_path, parse_dates=["event_date"])
    return assets, events


assets, events = load_data()
st.title("Dashboard Pemeliharaan Aset Infrastruktur")
st.caption("Demo interaktif untuk data sintetis — bukan data resmi pemerintah. Gunakan filter untuk menjawab pertanyaan operasional.")

# Sidebar controls remain visible and use familiar labels to reduce cognitive load.
st.sidebar.header("Filter data")
region_options = sorted(assets["region"].dropna().unique().tolist())
category_options = sorted(assets["category"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Wilayah", region_options, default=region_options)
selected_categories = st.sidebar.multiselect("Kategori aset", category_options, default=category_options)
min_date = events["event_date"].min().date()
max_date = events["event_date"].max().date()
date_value = st.sidebar.date_input("Rentang tanggal pemeliharaan", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_value, (tuple, list)) and len(date_value) == 2:
    date_start, date_end = pd.Timestamp(date_value[0]), pd.Timestamp(date_value[1])
else:
    date_start = date_end = pd.Timestamp(date_value)

assets_f = assets[assets["region"].isin(selected_regions) & assets["category"].isin(selected_categories)].copy()
events_f = events[
    events["region"].isin(selected_regions)
    & events["category"].isin(selected_categories)
    & events["event_date"].between(date_start, date_end)
].copy()

if assets_f.empty:
    st.warning("Tidak ada aset yang cocok dengan filter. Pilih kembali wilayah atau kategori di panel kiri.")
    st.stop()

# Summary cards make the most important information visible before users inspect details.
total_assets = assets_f["asset_id"].nunique()
critical_assets = int(assets_f["condition"].eq("Kritis").sum())
total_cost = float(events_f["maintenance_cost"].sum()) if not events_f.empty else 0.0
avg_downtime = float(events_f["downtime_hours"].mean()) if not events_f.empty else 0.0
k1, k2, k3, k4 = st.columns(4)
k1.metric("Jumlah aset", f"{total_assets:,}")
k2.metric("Aset berstatus kritis", f"{critical_assets:,}")
k3.metric("Biaya pemeliharaan", f"Rp {total_cost:,.0f}".replace(",", "."))
k4.metric("Rata-rata downtime", f"{avg_downtime:.1f} jam")

st.divider()
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Tren biaya pemeliharaan")
    if events_f.empty:
        st.info("Tidak ada catatan pemeliharaan pada rentang tanggal ini.")
    else:
        monthly = events_f.assign(month=events_f["event_date"].dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False)["maintenance_cost"].sum()
        fig = px.line(monthly, x="month", y="maintenance_cost", markers=True,
                      labels={"month": "Bulan", "maintenance_cost": "Biaya (Rp)"},
                      title="Perubahan biaya dari waktu ke waktu")
        fig.update_layout(margin=dict(l=15, r=15, t=50, b=15), yaxis_tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)
with col_right:
    st.subheader("Jumlah aset per kategori")
    counts = assets_f.groupby("category", as_index=False)["asset_id"].nunique().rename(columns={"asset_id": "jumlah_aset"})
    fig = px.bar(counts, x="category", y="jumlah_aset", text="jumlah_aset",
                 labels={"category": "Kategori", "jumlah_aset": "Jumlah aset"}, title="Perbandingan antar kategori")
    fig.update_layout(margin=dict(l=15, r=15, t=50, b=15), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

col_left2, col_right2 = st.columns(2)
with col_left2:
    st.subheader("Kondisi aset saat ini")
    condition_order = [x for x in ["Baik", "Perlu Perbaikan", "Kritis"] if x in assets_f["condition"].unique()]
    condition_counts = assets_f["condition"].value_counts().reindex(condition_order, fill_value=0).rename_axis("condition").reset_index(name="jumlah")
    fig = px.pie(condition_counts, names="condition", values="jumlah", hole=0.42,
                 title="Proporsi kondisi aset", labels={"condition": "Kondisi", "jumlah": "Jumlah aset"})
    fig.update_layout(margin=dict(l=15, r=15, t=50, b=15))
    st.plotly_chart(fig, use_container_width=True)
with col_right2:
    st.subheader("Biaya vs downtime")
    if events_f.empty:
        st.info("Tidak ada data untuk ditampilkan pada filter saat ini.")
    else:
        fig = px.scatter(events_f, x="downtime_hours", y="maintenance_cost", color="category",
                         hover_data=["asset_id", "event_date", "issue", "region"],
                         labels={"downtime_hours": "Downtime (jam)", "maintenance_cost": "Biaya (Rp)", "category": "Kategori"},
                         title="Setiap titik mewakili satu kejadian pemeliharaan")
        fig.update_layout(margin=dict(l=15, r=15, t=50, b=15), yaxis_tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Daftar aset dan detail pemeliharaan")
assets_table = assets_f.sort_values(["condition_score", "asset_name"], ascending=[True, True]).copy()
assets_table["usia_aset_tahun"] = (pd.Timestamp.today().normalize() - assets_table["installation_date"]).dt.days // 365
assets_table = assets_table[["asset_id", "asset_name", "region", "category", "condition", "condition_score", "usia_aset_tahun", "last_inspection"]]
st.dataframe(assets_table, use_container_width=True, hide_index=True)
st.download_button("Unduh data aset terfilter (CSV)", data=assets_table.to_csv(index=False).encode("utf-8"),
                   file_name="aset_terfilter.csv", mime="text/csv")

with st.expander("Lihat kejadian pemeliharaan secara rinci"):
    if events_f.empty:
        st.write("Tidak ada catatan pemeliharaan yang sesuai dengan filter.")
    else:
        detailed = events_f.sort_values("event_date", ascending=False)[
            ["event_id", "event_date", "asset_id", "region", "category", "issue", "maintenance_cost", "downtime_hours", "condition"]
        ]
        st.dataframe(detailed, use_container_width=True, hide_index=True)
        st.download_button("Unduh catatan terfilter (CSV)", data=detailed.to_csv(index=False).encode("utf-8"),
                           file_name="pemeliharaan_terfilter.csv", mime="text/csv")

st.caption("Prinsip desain: ringkasan lebih dulu, filter terlihat, grafik dipilih sesuai jenis pertanyaan, detail tersedia saat diminta, dan tidak ada efek dekoratif yang mengaburkan data.")
