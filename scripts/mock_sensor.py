import psycopg2
import random
import time
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="ep-square-mode-aev6ujkw-pooler.c-2.us-east-2.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="npg_YGSQ8cMUL7gq",
    sslmode="require"
)

cur = conn.cursor()

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

    print(f"[{datetime.now()}] Inserted data for {equipment_id}")
    time.sleep(2)  # every 2 seconds

cur.close()
conn.close()

