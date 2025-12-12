# Placeholder for anomaly detection

import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect simple anomalies using threshold rules:
      - Overheating: temp_c > 95
      - Low pressure: AHS < 10 bar, Drill < 15 bar
      - High vibration: Drill vibration_mms > 8
      - Speed anomaly: AHS speed_kmh > 55 when engine_load_pct < 30
    Returns a DataFrame with anomaly records.
    """
    records = []

    # Ensure expected columns exist
    required = ["timestamp","machine_id","machine_type","temp_c","pressure_bar",
                "vibration_mms","speed_kmh","engine_load_pct"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns for anomaly detection: {missing}")

    for _, row in df.iterrows():
        ts = row["timestamp"]
        mid = row["machine_id"]
        mtype = row["machine_type"]

        # Overheating
        if row["temp_c"] > 95:
            records.append({
                "timestamp": ts, "machine_id": mid, "machine_type": mtype,
                "anomaly": "Overheating", "value": row["temp_c"], "threshold": 95,
                "severity": "High", "recommendation": "Schedule cooling & inspect coolant/filters"
            })

        # Low pressure (type-specific)
        if mtype == "AHS" and row["pressure_bar"] < 10:
            records.append({
                "timestamp": ts, "machine_id": mid, "machine_type": mtype,
                "anomaly": "Low Pressure", "value": row["pressure_bar"], "threshold": 10,
                "severity": "Medium", "recommendation": "Check pump lines and pressure sensors"
            })
        if mtype == "Drill" and row["pressure_bar"] < 15:
            records.append({
                "timestamp": ts, "machine_id": mid, "machine_type": mtype,
                "anomaly": "Low Pressure", "value": row["pressure_bar"], "threshold": 15,
                "severity": "Medium", "recommendation": "Inspect hydraulic system & seals"
            })

        # High vibration (Drill)
        if mtype == "Drill" and row["vibration_mms"] > 8:
            records.append({
                "timestamp": ts, "machine_id": mid, "machine_type": mtype,
                "anomaly": "High Vibration", "value": row["vibration_mms"], "threshold": 8,
                "severity": "Medium", "recommendation": "Check bit wear and mounting"
            })

        # Speed anomaly (AHS)
        if mtype == "AHS" and (row["speed_kmh"] > 55) and (row["engine_load_pct"] < 30):
            records.append({
                "timestamp": ts, "machine_id": mid, "machine_type": mtype,
                "anomaly": "Speed/Load Mismatch", "value": row["speed_kmh"], "threshold": 55,
                "severity": "Low", "recommendation": "Validate load sensor, review operation profile"
            })

    anomalies = pd.DataFrame(records)
    if not anomalies.empty:
        anomalies = anomalies.sort_values(["timestamp","machine_id"]).reset_index(drop=True)
    return anomalies

def main():
    df = pd.read_csv("data/simulated_readings.csv", parse_dates=["timestamp"])
    anomalies = detect_anomalies(df)
    print(f"\nFound {len(anomalies)} anomalies")
    if not anomalies.empty:
        print(anomalies.head().to_string(index=False))

if __name__ == "__main__":
    main()
