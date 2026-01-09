import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURATION
# ----------------
DB_NAME = 'thor_telemetry.db'  # Check if your file is named differently!
TABLE_NAME = 'race_data'       # Check your table name!

# 2. LOAD DATA
# ------------
print(f"--- Connecting to {DB_NAME} ---")
conn = sqlite3.connect(DB_NAME)

# We grab Lap, Timestamp, and Fuel. 
# We ignore everything else to keep it fast.
query = f"SELECT lap, timestamp, fuel_kg FROM {TABLE_NAME} ORDER BY timestamp ASC"
df = pd.read_sql_query(query, conn)
conn.close()

# 3. CALCULATE LAP TIMES (The Data Science Part)
# ---------------------------------------------
# Since we have raw ticks, we need to group by 'Lap' to find the start/end of each lap.
print("--- Processing Lap Data ---")

results = []

# Get a list of all unique laps (e.g., 1, 2, 3... 19)
unique_laps = df['lap'].unique()

for lap in unique_laps:
    # Filter data for just this lap
    lap_data = df[df['lap'] == lap]
    
    # Calculate Duration: (End Time - Start Time)
    # Note: This assumes timestamp is in Seconds. 
    duration = lap_data['timestamp'].max() - lap_data['timestamp'].min()
    
    # Get Average Fuel for this lap
    avg_fuel = lap_data['fuel_kg'].mean()
    
    # Store it
    results.append({
        'Lap': lap,
        'LapTime': duration,
        'Fuel': avg_fuel
    })

# Convert our list of results into a clean Table (DataFrame)
results_df = pd.DataFrame(results)

# Filter out Lap 1 (Warm up is usually slow and messes up the scale)
results_df = results_df[results_df['Lap'] > 1]

print(results_df)

# 4. GENERATE THE CHART
# ---------------------
print("--- Generating Graph ---")

fig, ax1 = plt.subplots(figsize=(10, 6))

title = "Audi R18: Fuel Load vs. Lap Time (Spa Francorchamps)"
plt.title(title, fontsize=14, fontweight='bold')

# Axis 1: Lap Times (Red Line)
color = 'tab:red'
ax1.set_xlabel('Lap Number')
ax1.set_ylabel('Lap Time (Seconds)', color=color)
ax1.plot(results_df['Lap'], results_df['LapTime'], color=color, marker='o', linewidth=2, label='Lap Time')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3)

# Axis 2: Fuel Load (Blue Line) -> We create a second Y-axis that shares the same X-axis
ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Fuel Level (Liters)', color=color)
ax2.plot(results_df['Lap'], results_df['Fuel'], color=color, linestyle='--', linewidth=2, label='Fuel Level')
ax2.tick_params(axis='y', labelcolor=color)

# Show the graph
plt.tight_layout()
plt.show()