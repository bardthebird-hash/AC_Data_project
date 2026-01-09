import sqlite3

conn = sqlite3.connect('thor_telemetry.db')
cursor = conn.cursor()

# 1. Delete data where the car hasn't moved yet (Start of race)
cursor.execute("""
    DELETE FROM race_data 
    WHERE timestamp < (SELECT MIN(timestamp) FROM race_data WHERE speed_kmh > 5)
""")

# 2. Delete the 'Victory' data after the finish line (if you kept recording)
# cursor.execute("DELETE FROM race_data WHERE lap > 10")

conn.commit()
conn.close()
print("Data cleaned. Pre-race stationary data removed.")
