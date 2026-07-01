import pandas as pd
import sqlite3

# 1. Connect to your massive SQLite database
# (Change 'transit.db' to your actual database filename)
conn = sqlite3.connect('data.db')

# 2. Read ONLY the necessary columns from the CSV to save memory
print("Loading CSV...")
df_coords = pd.read_csv(
    'place_master.csv', 
    usecols=['PLACE_ID', 'LATITUDE', 'LONGITUDE']
)

# 3. Clean up column names to match standard SQL lowercase format
df_coords.columns = ['place_id', 'latitude', 'longitude']

# Drop any rows that are missing coordinates (prevents map errors later)
df_coords = df_coords.dropna(subset=['latitude', 'longitude'])

# 4. Push this DataFrame into SQLite as a new table
print("Writing to SQLite database...")
df_coords.to_sql('place_coordinates', conn, if_exists='replace', index=False)

# 5. CRITICAL: Create an index so Streamlit maps load instantly
print("Creating database index...")
cursor = conn.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS idx_place_id ON place_coordinates(place_id)')
conn.commit()

print("Success! Coordinates are now locked into the database.")
conn.close()