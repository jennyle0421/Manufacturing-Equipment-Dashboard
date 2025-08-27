import os
import psycopg2
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ---------------------
# STREAMLIT PAGE CONFIG
# ---------------------
st.set_page_config(
    page_title="🏭 Manufacturing Equipment Dashboard",
    layout="wide"
)

st.title("🏭 Manufacturing Equipment Dashboard")
st.write("Live monitoring of **temperature**, **vibration**, and **throughput** metrics.")

# ---------------------
# AUTO-REFRESH FEATURE
# ---------------------
# Refresh dashboard every 5 seconds
st_autorefresh(interval=5000, key="data_refresh")

# ---------------------
# DATABASE CONNECTION
# ---------------------
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        port=st.secrets["DB_PORT"],
        sslmode="require"   # Neon requires SSL
    )

# ---------------------
# LOAD LATEST DATA
# ---------------------
def load_data():
    query = """
        SELECT * FROM equipment_data
        ORDER BY recorded_at DESC
        LIMIT 50
    """
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error("⚠️ Failed to fetch data from the database.")
        st.exception(e)
        return pd.DataFrame()

df = load_data()

# ---------------------
# HANDLE EMPTY DATA
# ---------------------
if df.empty:
    st.warning("⚠️ No data available yet. Start mock_sensor.py to generate live data.")
    st.stop()

# Convert recorded_at to datetime for charts
df["recorded_at"] = pd.to_datetime(df["recorded_at"])

# ---------------------
# CRITICAL ALERT COUNTERS
# ---------------------
critical_temp = df[df["temperature"] > 100].shape[0]
critical_vibe = df[df["vibration"] > 2.0].shape[0]

col1, col2 = st.columns(2)
col1.metric("🔥 Overheating Machines", critical_temp)
col2.metric("⚡ High-Vibration Machines", critical_vibe)

# ---------------------
# HIGHLIGHT CRITICAL ALERTS IN TABLE
# ---------------------
def highlight_alerts(row):
    color = ""
    if row["temperature"] > 100:
        color = "background-color: #ff4d4d; color: white"  # Red for overheating
    elif row["vibration"] > 2.0:
        color = "background-color: #ff944d; color: white"  # Orange for high vibration
    return [color] * len(row)

st.subheader("Latest Equipment Data")
st.dataframe(df.style.apply(highlight_alerts, axis=1), use_container_width=True)

# ---------------------
# VISUAL CHARTS
# ---------------------
st.subheader("Temperature Trends")
st.line_chart(df.set_index("recorded_at")["temperature"])

st.subheader("Vibration Trends")
st.line_chart(df.set_index("recorded_at")["vibration"])

st.subheader("Throughput Trends")
st.line_chart(df.set_index("recorded_at")["throughput"])
