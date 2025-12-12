# Placeholder for data simulation logic

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


# Configuration

np.random.seed(42)

NUM_MACHINES = 8                 # total machines in fleet
DAYS = 1                         # simulate one day
MINUTES = DAYS * 24 * 60         # 1440 minutes
START_TIME = datetime.now().replace(second=0, microsecond=0) - timedelta(days=DAYS)

OUTPUT_DIR = os.path.join("data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "simulated_readings.csv")


# Helpers

def simulate_series(length, base, noise, drift=0.0, lower=None, upper=None):
    """Noisy time series with optional drift and bounds."""
    series = base + np.random.normal(0, noise, length) + np.linspace(0, drift, length)
    if lower is not None:
        series = np.maximum(series, lower)
    if upper is not None:
        series = np.minimum(series, upper)
    return series

def simulate_machine(machine_id, machine_type):
    """Simulate one machine timeline with sensor readings."""
    timestamps = [START_TIME + timedelta(minutes=m) for m in range(MINUTES)]

    # Operational status: 1=operating, 0=idle, 2=maintenance, 3=downtime
    status = np.random.choice([0, 1, 2, 3], size=MINUTES, p=[0.15, 0.65, 0.10, 0.10])

    # Speed (km/h): relevant for trucks, zero for drills
    if machine_type == "AHS":
        speed = simulate_series(MINUTES, base=30, noise=8, lower=0, upper=60)
        speed = np.where(status != 1, 0, speed)  # move only when operating
    else:
        speed = np.zeros(MINUTES)

    # Fuel rate (L/h): higher when operating, low otherwise
    fuel_base = 40 if machine_type == "AHS" else 15
    fuel_rate = simulate_series(MINUTES, base=fuel_base, noise=5, lower=0)
    fuel_rate = np.where(status == 1, fuel_rate, fuel_rate * 0.25)

    # Temperature (°C): gradual drift + occasional anomaly spikes
    temp = simulate_series(MINUTES, base=75, noise=3, drift=1.5, lower=50, upper=110)
    temp = np.where(status == 3, temp - 10, temp)   # cooler when down
    anomaly_idx = np.random.choice(MINUTES, size=int(MINUTES * 0.01), replace=False)
    temp[anomaly_idx] = temp[anomaly_idx] + np.random.uniform(8, 15, size=len(anomaly_idx))

    # Vibration (mm/s): higher under load for drills
    vib_base = 3 if machine_type == "AHS" else 6
    vibration = simulate_series(MINUTES, base=vib_base, noise=1.2, lower=0)
    vibration = np.where(status == 1, vibration * 1.2, vibration * 0.7)

    # Engine load (%) and pressure (bar)
    engine_load = simulate_series(MINUTES, base=55, noise=10, lower=0, upper=100)
    pressure = simulate_series(MINUTES, base=12 if machine_type == "AHS" else 20, noise=2, lower=5)

    # Derived flags
    overheating = (temp > 95).astype(int)
    low_pressure = (pressure < (10 if machine_type == "AHS" else 15)).astype(int)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "machine_id": machine_id,
        "machine_type": machine_type,
        "status": status,               # 0 idle, 1 operating, 2 maintenance, 3 downtime
        "speed_kmh": np.round(speed, 2),
        "fuel_lph": np.round(fuel_rate, 2),
        "temp_c": np.round(temp, 2),
        "vibration_mms": np.round(vibration, 2),
        "engine_load_pct": np.round(engine_load, 1),
        "pressure_bar": np.round(pressure, 2),
        "flag_overheating": overheating,
        "flag_low_pressure": low_pressure,
    })
    return df


# Main

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build machine list: half trucks, half drills
    half = NUM_MACHINES // 2
    machine_ids = [(f"AHS_{i:02d}", "AHS") for i in range(1, half + 1)] + \
                  [(f"Drill_{i:02d}", "Drill") for i in range(1, half + 1)]

    all_df = []
    for mid, mtype in machine_ids:
        all_df.append(simulate_machine(mid, mtype))

    df = pd.concat(all_df, ignore_index=True)

    # Sort by time then machine for neatness
    df.sort_values(["timestamp", "machine_id"], inplace=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Generated {len(df):,} rows for {len(machine_ids)} machines → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
