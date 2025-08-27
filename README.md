# 🏭 Manufacturing Equipment Dashboard

A real-time monitoring dashboard for manufacturing equipment using **Streamlit** and **PostgreSQL**.

## Features
- 📊 Live charts for **temperature**, **vibration**, and **throughput**
- 🔴 Highlights critical alerts automatically
- ⏱️ Auto-refresh every 5 seconds
- ✅ Mock data generation via `mock_sensor.py`

## How to Run
```bash
pip install -r requirements.txt
streamlit run scripts/dashboard.py
