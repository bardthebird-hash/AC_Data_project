import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to your Database
db_path = "thor_telemetry.db"
conn = sqlite3.connect(db_path)

# 2. Extract Data using SQL (The "Science" part)
# We only want the first 60 seconds of data to keep the graph readable
query = '''
SELECT session_time, speed_kmh, hybrid_deploy, throttle
FROM race_data 
WHERE session_time <= 60 
ORDER BY session_time ASC
'''

# Load into Pandas DataFrame
df = pd.read_sql_query(query, conn)
conn.close()

# 3. Visualization (The "Engineering" part)
fig, ax1 = plt.figure(figsize=(12, 6)), plt.gca()

# Plot Speed (Left Axis)
ax1.plot(df['session_time'], df['speed_kmh'], color='black', linewidth=1.5, label='Speed (km/h)')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Speed (km/h)', color='black')

# Create a second axis for Hybrid Deploy (Right Axis)
ax2 = ax1.twinx()
# Fill the area under the curve for Hybrid Deploy to look like telemetry software
ax2.fill_between(df['session_time'], df['hybrid_deploy'], color='green', alpha=0.3, label='Hybrid Deploy (0-1)')
ax2.set_ylabel('Hybrid Output', color='green')
ax2.set_ylim(0, 1.1) # Fix scale from 0 to 100%

# Add Title and Grid
plt.title('LMP1 Telemetry: Speed vs. Hybrid Deployment Profile')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Show the plot
plt.tight_layout()
plt.show()

print(f"Analyzed {len(df)} data points successfully.")