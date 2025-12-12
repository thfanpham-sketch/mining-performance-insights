```text
✅Mining Performance Insights: 
Python-based toolkit for mining operations analytics. This project provides:
Data Simulation: Generate realistic mining sensor data.
Fleet KPIs: Compute utilization, downtime, and maintenance metrics.
Anomaly Detection: Identify abnormal sensor readings.
Predictive Maintenance: Logistic regression model for failure risk prediction.

## 📂 Project Structure
```text
mining-ops-dashboard/
├─ data/
│  └─ simulated_readings.csv
├─ src/
│  ├─ simulation/
│  │  └─ generateData.js
│  ├─ analytics/
│  │  ├─ kpis.js
│  │  ├─ anomaly.js
│  │  └─ predict.js
│  ├─ utils/
│  │  └─ loadData.js
│  └─ dashboard.js
├─ reports/
├─ package.json
├─ README.md
└─ .gitignore
```
---

## 🚀 Features:
- **Data Simulation**
  - Generates realistic, multi-machine time-series data with status, sensors, and event flags.
- **Fleet KPIs**
  - Utilization %, downtime %, maintenance %, event counts, averages (fuel, speed, temp).
- **Anomaly Detection**
  - Flags and summarizes low pressure, high vibration, high temperature.
- **Predictive Maintenance**
  - Logistic Regression model with **classification report**, **confusion matrix**, **ROC**, and **Precision–Recall**.

## ✅ Requirements
Install Python packages:
pip install -r requirements.txt

▶ How to Run
1. Simulate Data
Generate a dataset: python .\src\simulation\generate_data.py
2. Compute KPIs
python .\src\analytics\kpis.py
3. Detect Anomalies:
ppython .\src\analytics\anomaly.py
4. Predictive Maintenance:
python .\src\analytics\predict.py


📝 License
MIT License.


