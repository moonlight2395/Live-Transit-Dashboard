import sqlite3
import pandas as pd
import datetime
import random

print("Generating Himachal Pradesh transit data...")

# 1. Authentic HP Locations
places = [
    {"id": 1, "name": "Shimla ISBT", "lat": 31.1048, "lon": 77.1734},
    {"id": 2, "name": "Manali Bus Stand", "lat": 32.2396, "lon": 77.1887},
    {"id": 3, "name": "Dharamshala Terminal", "lat": 32.2190, "lon": 76.3234},
    {"id": 4, "name": "Mandi Transit Hub", "lat": 31.5892, "lon": 76.9328},
    {"id": 5, "name": "Kullu Stop", "lat": 31.9579, "lon": 77.1095}
]

# Create Place and Coordinates DataFrames
df_place = pd.DataFrame([{"place_id": p["id"], "place_name": p["name"]} for p in places])
df_coords = pd.DataFrame([{"place_id": p["id"], "latitude": p["lat"], "longitude": p["lon"]} for p in places])

# 2. Generate 250 randomized trips for Oct 1, 2023
trips = []
base_time = datetime.datetime(2023, 10, 1, 5, 0, 0) # Starting at 5:00 AM

for i in range(250):
    place = random.choice(places)
    # Random scheduled time between 5 AM and 10 PM
    scheduled = base_time + datetime.timedelta(minutes=random.randint(0, 1020)) 
    
    # Simulate realistic delays
    delay_chance = random.random()
    if delay_chance < 0.60:   delay = random.randint(0, 5)   # 60% On-Time
    elif delay_chance < 0.85: delay = random.randint(6, 15)  # 25% Slight Delay
    else:                     delay = random.randint(16, 45) # 15% Heavy Delay
    
    actual = scheduled + datetime.timedelta(minutes=delay)
    
    trips.append({
        "id": 5000 + i,
        "route_id": f"HP-Route-{random.randint(1, 9)}",
        "start_place_id": place["id"],
        "scheduled_trip_start_time": scheduled.strftime('%Y-%m-%d %H:%M:%S'),
        "actual_trip_start_time": actual.strftime('%Y-%m-%d %H:%M:%S')
    })

df_trip = pd.DataFrame(trips)

# 3. Build the SQLite Database
db_name = "hp_sample.db"
conn = sqlite3.connect(db_name)

df_place.to_sql("place", conn, index=False, if_exists="replace")
df_coords.to_sql("place_coordinates", conn, index=False, if_exists="replace")
df_trip.to_sql("trip", conn, index=False, if_exists="replace")

conn.close()
print(f"Success! {db_name} has been created in your folder.")
