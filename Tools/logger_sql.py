import time
import sqlite3
from Sim_info import SimInfo

# --- CONFIGURATION ---
DB_NAME = "thor_telemetry.db"
SAMPLE_RATE = 0.05  # 20Hz
COMMIT_INTERVAL = 100 # Save to disk every 100 rows (Optimization)

# 1. Setup Database Connection
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 2. Create the Table (The Schema)
# This defines the "buckets" for your data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS race_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        session_time REAL,
        lap INTEGER,
        position INTEGER,
        speed_kmh REAL,
        throttle REAL,
        brake REAL,
        gear INTEGER,
        rpm INTEGER,
        steer_angle REAL,
        hybrid_charge REAL,
        hybrid_deploy REAL,
        tyre_wear_fl REAL,
        tyre_wear_fr REAL,
        tyre_wear_rl REAL,
        tyre_wear_rr REAL,
        fuel_kg REAL,
        x_coord REAL,
        z_coord REAL
    )
''')
conn.commit()
print(f"Database connected: {DB_NAME}")

# 3. Connect to Game
info = SimInfo()
print("Waiting for Assetto Corsa physics...")

start_time = None
row_count = 0

try:
    while True:
        # Check if physics are active
        if info.static.playerNick:
            
            # Initialize Start Time on first frame
            if start_time is None:
                start_time = time.time()
                print("Green Flag! Logging started...")

            current_time = time.time()
            session_time = current_time - start_time
            
            phy = info.physics
            gfx = info.graphics

            # Prepare the SQL Query
            sql = '''INSERT INTO race_data (
                        timestamp, session_time, lap, position, speed_kmh, 
                        throttle, brake, gear, rpm, steer_angle, 
                        hybrid_charge, hybrid_deploy, 
                        tyre_wear_fl, tyre_wear_fr, tyre_wear_rl, tyre_wear_rr, 
                        fuel_kg, x_coord, z_coord
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            
            # The Data Packet
            data = (
                current_time,
                round(session_time, 3), # The graph-friendly time
                gfx.completedLaps,
                gfx.position,
                round(phy.speedKmh, 2),
                round(phy.gas, 3),
                round(phy.brake, 3),
                phy.gear,
                phy.rpms,
                round(phy.steerAngle, 3),
                round(phy.kersCharge, 3),
                round(phy.kersInput, 3),
                round(phy.tyreWear[0], 1),
                round(phy.tyreWear[1], 1),
                round(phy.tyreWear[2], 1),
                round(phy.tyreWear[3], 1),
                round(phy.fuel, 2),
                round(gfx.carCoordinates[0], 2), # Corrected attribute name
                round(gfx.carCoordinates[2], 2)
            )

            cursor.execute(sql, data)
            row_count += 1

            # Optimization: Only write to hard drive every 100 rows
            if row_count % COMMIT_INTERVAL == 0:
                conn.commit()
                print(f"\rLogged {row_count} rows...", end="")

            time.sleep(SAMPLE_RATE)
        else:
            time.sleep(1)

except KeyboardInterrupt:
    conn.commit() # Force save remaining data
    conn.close()
    print(f"\nSession saved to {DB_NAME}. Total rows: {row_count}")
