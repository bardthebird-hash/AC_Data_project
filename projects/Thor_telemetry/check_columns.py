import sqlite3

# Connect to your database
conn = sqlite3.connect('thor_telemetry.db')
cursor = conn.cursor()

# Get the table info
# (Make sure 'race_data' is the right table name based on your error log)
cursor.execute("PRAGMA table_info(race_data)")
columns = cursor.fetchall()

print("--- YOUR COLUMNS ---")
for col in columns:
    print(col[1])  # This prints the column name

conn.close()