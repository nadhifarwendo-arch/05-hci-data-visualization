"""Create small synthetic infrastructure-asset and maintenance data for the demo."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = np.random.default_rng(205077)


def main():
    DATA.mkdir(exist_ok=True)
    n_assets = 150
    regions = ["Teluk Segara", "Ratu Agung", "Gading Cempaka", "Selebar", "Muara Bangkahulu", "Sungai Serut"]
    categories = ["Jalan", "Drainase", "Jembatan", "Lampu Jalan", "Gedung"]
    assets = []
    for i in range(1, n_assets + 1):
        install_year = int(RNG.integers(2008, 2025))
        score = int(np.clip(RNG.normal(76, 17), 20, 100))
        condition = "Baik" if score >= 75 else ("Perlu Perbaikan" if score >= 50 else "Kritis")
        assets.append({
            "asset_id": f"AST-{i:04d}",
            "asset_name": f"Aset Infrastruktur {i:03d}",
            "region": str(RNG.choice(regions)),
            "category": str(RNG.choice(categories, p=[0.27, 0.25, 0.12, 0.22, 0.14])),
            "installation_date": f"{install_year}-{int(RNG.integers(1,13)):02d}-{int(RNG.integers(1,28)):02d}",
            "condition_score": score,
            "condition": condition,
            "last_inspection": pd.Timestamp("2026-10-01") - pd.Timedelta(days=int(RNG.integers(0, 330))),
        })
    asset_df = pd.DataFrame(assets)
    asset_df["last_inspection"] = pd.to_datetime(asset_df["last_inspection"]).dt.strftime("%Y-%m-%d")

    issue_map = {
        "Jalan": ["Retak permukaan", "Lubang jalan", "Genangan"],
        "Drainase": ["Sumbatan", "Dinding rusak", "Sedimentasi"],
        "Jembatan": ["Korosi", "Sambungan longgar", "Pemeriksaan rutin"],
        "Lampu Jalan": ["Lampu mati", "Kabel bermasalah", "Pemeriksaan rutin"],
        "Gedung": ["Kebocoran", "Perbaikan instalasi", "Pemeriksaan rutin"],
    }
    events = []
    event_id = 1
    for a in assets:
        count = int(RNG.integers(1, 7))
        base_date = pd.Timestamp("2024-11-01")
        for _ in range(count):
            event_date = base_date + pd.Timedelta(days=int(RNG.integers(0, 700)))
            issue = str(RNG.choice(issue_map[a["category"]]))
            risk_multiplier = 1.7 if a["condition"] == "Kritis" else (1.2 if a["condition"] == "Perlu Perbaikan" else 0.8)
            base_cost = {"Jalan": 2_500_000, "Drainase": 1_800_000, "Jembatan": 5_000_000,
                         "Lampu Jalan": 850_000, "Gedung": 3_000_000}[a["category"]]
            cost = round(float(RNG.lognormal(np.log(base_cost * risk_multiplier), 0.45)), -3)
            downtime = round(float(RNG.gamma(2.0, 4.0) * risk_multiplier), 1)
            events.append({
                "event_id": f"EVT-{event_id:05d}",
                "asset_id": a["asset_id"],
                "event_date": event_date.strftime("%Y-%m-%d"),
                "issue": issue,
                "maintenance_cost": max(100_000, cost),
                "downtime_hours": downtime,
            })
            event_id += 1
    events_df = pd.DataFrame(events).merge(asset_df[["asset_id", "region", "category", "condition"]], on="asset_id", how="left", validate="many_to_one")
    asset_df.to_csv(DATA / "assets.csv", index=False)
    events_df.to_csv(DATA / "maintenance_events.csv", index=False)
    print(f"Created {len(asset_df)} assets and {len(events_df)} maintenance records in {DATA}")

if __name__ == "__main__":
    main()
