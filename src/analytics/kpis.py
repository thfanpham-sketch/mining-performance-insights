# Placeholder for KPI calculations

import pandas as pd

INPUT_FILE = "data/simulated_readings.csv"

def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute KPIs per machine:
      - utilization_pct: % of rows where status == 1 (operating)
      - downtime_pct: % of rows where status == 3 (downtime)
      - maintenance_pct: % of rows where status == 2 (maintenance)
      - overheating_events: count of flag_overheating == 1
    """
    # Map statuses for readability
    # 0 idle, 1 operating, 2 maintenance, 3 downtime
    def pct(series, code):
        return (series == code).mean() * 100.0

    grouped = df.groupby(["machine_id", "machine_type"])

    results = grouped.apply(lambda g: pd.Series({
        "utilization_pct": round(pct(g["status"], 1), 2),
        "downtime_pct": round(pct(g["status"], 3), 2),
        "maintenance_pct": round(pct(g["status"], 2), 2),
        "overheating_events": int(g["flag_overheating"].sum()),
        "low_pressure_events": int(g["flag_low_pressure"].sum()),
        "avg_fuel_lph": round(g["fuel_lph"].mean(), 2),
        "avg_speed_kmh": round(g["speed_kmh"].mean(), 2),
        "avg_temp_c": round(g["temp_c"].mean(), 2),
    })).reset_index()

    return results.sort_values("machine_id")

def compute_overall(df: pd.DataFrame) -> dict:
    """Overall fleet-level KPIs."""
    total = len(df)
    overall = {
        "fleet_utilization_pct": round((df["status"] == 1).mean() * 100.0, 2),
        "fleet_downtime_pct": round((df["status"] == 3).mean() * 100.0, 2),
        "fleet_maintenance_pct": round((df["status"] == 2).mean() * 100.0, 2),
        "overheating_events": int(df["flag_overheating"].sum()),
        "low_pressure_events": int(df["flag_low_pressure"].sum()),
        "rows": total,
        "machines": df["machine_id"].nunique(),
        "time_range": f"{df['timestamp'].min()} → {df['timestamp'].max()}",
    }
    return overall

def main():
    # Load the CSV
    df = pd.read_csv(INPUT_FILE, parse_dates=["timestamp"])

    per_machine = compute_kpis(df)
    overall = compute_overall(df)

    # Print results to console (simple & fast)
    print("\n=== Fleet Overview ===")
    for k, v in overall.items():
        print(f"{k}: {v}")

    print("\n=== KPIs per Machine ===")
    print(per_machine.to_string(index=False))

if __name__ == "__main__":
    main()
