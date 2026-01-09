import time
import csv
import os
from Sim_info import SimInfo

# --- CONFIGURATION ---
# We use "R18_P4_Analysis" to label this specific dataset based on your result
SESSION_LABEL = "R18_Silverstone_MixedGrid" 
SAMPLE_RATE = 0.05 # 20Hz (Standard for initial analysis)

info = SimInfo()
print(f"Searching for Assetto Corsa... (Waiting for Green Flag)")

# Create 'data' folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Generate filename: data/R18_Silverstone_20240521-1430.csv
timestamp = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/{SESSION_LABEL}_{timestamp}.csv"

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # The Header Row - These are the columns for your Data Science Project
    headers = [
        "Time", "Lap", "Position", "Speed_Kmh", 
        "Throttle", "Brake", "Gear", "RPM",
        "SteerAngle", 
        "Hybrid_Charge", "Hybrid_Deploy", # Crucial for LMP1 vs Valkyrie
        "TireWear_FL", "TireWear_FR", "TireWear_RL", "TireWear_RR",
        "Fuel_Kg",
        "X_Coord", "Y_Coord", "Z_Coord" # For mapping the track
    ]
    writer.writerow(headers)
    print(f"Logging started! Saving to: {filename}")

    try:
        while True:
            # only log if physics engine is active
            if info.static.playerNick: 
                phy = info.physics
                gfx = info.graphics
                
                row = [
                    time.time(),
                    gfx.completedLaps,
                    gfx.position,
                    round(phy.speedKmh, 2),
                    round(phy.gas, 3),
                    round(phy.brake, 3),
                    phy.gear,
                    phy.rpms,
                    round(phy.steerAngle, 3),
                    
                    # Hybrid Data (0-1 Scale)
                    round(phy.kersCharge, 3),
                    round(phy.kersInput, 3),
                    
                    # Tire Wear (98.0 = 98%)
                    round(phy.tyreWear[0], 1),
                    round(phy.tyreWear[1], 1),
                    round(phy.tyreWear[2], 1),
                    round(phy.tyreWear[3], 1),
                    
                    round(phy.fuel, 2),
                    
                    # Coordinates for Heatmaps  
                    round(gfx.carCoordinates[0], 2),
                    round(gfx.carCoordinates[1], 2),
                    round(gfx.carCoordinates[2], 2)
                ]
                writer.writerow(row)
                time.sleep(SAMPLE_RATE)
            else:
                # Poll slower if game is paused/menu
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\nSTOPPED. Data saved successfully to {filename}")