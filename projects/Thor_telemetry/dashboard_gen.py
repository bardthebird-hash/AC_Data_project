import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect
conn = sqlite3.connect('thor_telemetry.db')
df = pd.read_sql_query("SELECT * FROM race_data", conn)
conn.close()

# Grouping
lap_stats = df.groupby('lap').agg({'speed_kmh': 'max', 'fuel_kg': 'mean', 'tyre_wear_fl': 'mean'}).reset_index()
lap_stats = lap_stats[lap_stats['lap'] > 1] # Skip warm-up

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
plt.subplots_adjust(hspace=0.4)

# Chart 1: Degradation
ax1.plot(lap_stats['lap'], lap_stats['speed_kmh'], color='red', marker='o', label='Max Speed')
ax1_tw = ax1.twinx()
ax1_tw.plot(lap_stats['lap'], lap_stats['tyre_wear_fl'], color='green', linestyle='--')
ax1.set_title("Top Speed vs Tyre Wear (Grip Loss)")

# Chart 2: Weight
ax2.plot(lap_stats['lap'], lap_stats['speed_kmh'], color='red', marker='o')
ax2_tw = ax2.twinx()
ax2_tw.plot(lap_stats['lap'], lap_stats['fuel_kg'], color='blue', linestyle='--')
ax2.set_title("Top Speed vs Fuel Weight (Mass Reduction)")

# Chart 3: The Event Map (Yellow Flag & Battle)
ax3.scatter(df['lap'], df['speed_kmh'], alpha=0.1, s=1, color='purple')
ax3.set_title("Full Speed Distribution (Events Visible)")



plt.savefig('race_analysis_report.png')
plt.show()