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
    try:
        return psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASS"],
            port=st.secrets["DB_PORT"],
            sslmode="require"
        )
    except Exception as e:
        st.error(f"⚠️ Failed to connect to the database: {e}")
        st.stop()

# ---------------------
# FETCH DATA
# ---------------------
def load_data():
    try:
        conn = get_connection()
        query = """
            SELECT *
            FROM equipment_data
            ORDER BY created_at DESC
            LIMIT 50
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Failed to fetch data from the database.\n\nError: {e}")
        return pd.DataFrame()

df = load_data()

# ---------------------
# DISPLAY DASHBOARD
# ---------------------
if df.empty:
    st.warning("⚠️ No data available yet. Start `mock_sensor.py` to generate live data.")
else:
    st.subheader("📊 Latest Equipment Data")

    # ---------------------
    # HIGHLIGHT CRITICAL VALUES
    # ---------------------
    def highlight_values(val, column):
        if column == "temperature":
            return "background-color: red; color: white;" if val > 100 else ""
        elif column == "vibration":
            return "background-color: orange; color: black;" if val > 2.0 else ""
        elif column == "throughput":
            return "background-color: #007BFF; color: white;" if val < 100 else ""
        return ""

    def highlight_dataframe(df):
        return df.style.apply(
            lambda col: [highlight_values(v, col.name) for v in col],
            axis=0
        )

    styled_df = highlight_dataframe(df)
    st.dataframe(styled_df, use_container_width=True)

    # ---------------------
    # METRICS OVERVIEW
    # ---------------------
    st.subheader("🔍 Metrics Overview")

    col1, col2, col3 = st.columns(3)

    avg_temp = df["temperature"].mean()
    avg_vib = df["vibration"].mean()
    avg_throughput = df["throughput"].mean()

    col1.metric("🌡️ Avg Temperature (°F)", f"{avg_temp:.2f}")
    col2.metric("📳 Avg Vibration (mm/s)", f"{avg_vib:.2f}")
    col3.metric("⚡ Avg Throughput (units/hr)", f"{avg_throughput:.2f}")

    # ---------------------
    # VISUALIZATIONS
    # ---------------------
    st.subheader("📈 Temperature Trends")
    st.line_chart(df.set_index("created_at")["temperature"])

    st.subheader("📈 Vibration Trends")
    st.line_chart(df.set_index("created_at")["vibration"])

    st.subheader("📈 Throughput Trends")
    st.line_chart(df.set_index("created_at")["throughput"])
