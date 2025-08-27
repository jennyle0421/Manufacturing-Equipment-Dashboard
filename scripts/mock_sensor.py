import psycopg2
import random
import time
from datetime import datetime
import toml
import os

# ---------------------
# LOAD DATABASE SECRETS
# ---------------------
# Load secrets.toml manually
secrets_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".streamlit",
    "secrets.toml"
)

if not os.path.exists(secrets_path):
    raise FileNotFoundError(
        f"❌ Could not find secrets.toml at: {secrets_path}\n"
        "Make sure your .streamlit/secrets.toml file exists and contains DB credentials."
    )

secrets = toml.load(secrets_path)

DB_HOST = secrets["DB_HOST"]
DB_NAME = secrets["DB_NAME"]
DB_USER = secrets["DB_USER"]
DB_PASS = secrets["DB_PASS"]
DB_PORT = secrets["DB_PORT"]

# ---------------------
# DATABASE CONNECTION
# ---------------------
def get_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            sslmode="require"
        )
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")
        exit(1)

# ---------------------
# INSERT RANDOM DATA
# ---------------------
def insert_mock_data():
    conn = get_connection()
    cur = conn.cursor()

    try:
        while True:
            equipment_id = random.choice(["EQ-001", "EQ-002", "EQ-003"])
            temperature = round(random.uniform(60, 120), 2)  # °F
            vibration = round(random.uniform(0.1, 2.5), 2)   # mm/s
            throughput = random.randint(80, 200)             # units/hr

            cur.execute("""
                INSERT INTO equipment_data (equipment_id, temperature, vibration, throughput)
                VALUES (%s, %s, %s, %s)
            """, (equipment_id, temperature, vibration, throughput))

            conn.commit()

            print(f"[{datetime.now()}] ✅ Inserted data for {equipment_id} | "
                  f"Temp: {temperature}°F | Vib: {vibration}mm/s | Throughput: {throughput}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n🛑 Stopping data generation...")
    finally:
        cur.close()
        conn.close()

# ---------------------
# MAIN ENTRY POINT
# ---------------------
if __name__ == "__main__":
    print("🚀 Starting mock sensor data generator...")
    insert_mock_data()
