# Placeholder for predictive maintenance model

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

INPUT_FILE = "data/simulated_readings.csv"
FEATURES = ["speed_kmh","fuel_lph","temp_c","vibration_mms","engine_load_pct","pressure_bar","status"]

def main():
    df = pd.read_csv(INPUT_FILE)
    # Label: overheating or low pressure
    df["fail_risk"] = ((df["flag_overheating"] == 1) | (df["flag_low_pressure"] == 1)).astype(int)

    X = df[FEATURES]
    y = df["fail_risk"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n=== Predictive Maintenance Model Report ===")
    print(classification_report(y_test, y_pred, digits=3))

if __name__ == "__main__":
    main()
