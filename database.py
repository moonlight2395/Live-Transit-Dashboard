import sqlite3
import pandas as pd

def get_daily_trips(target_date, db_path='data.db'):
    """
    Fetches trip data joined with coordinates for a specific date 
    from a specified SQLite database file path.
    """
    conn = sqlite3.connect(db_path)
    
    # Keeping your coordinate flip logic perfectly intact so the maps stay in AP
    query = """
    SELECT 
        t.route_id,
        p.place_id AS place_id,
        t.scheduled_trip_start_time AS scheduled_start,
        t.actual_trip_start_time AS actual_start,
        p.place_name,
        c.latitude AS longitude,  
        c.longitude AS latitude   
    FROM trip t
    JOIN place p ON t.start_place_id = p.place_id
    JOIN place_coordinates c ON p.place_id = c.place_id
    WHERE DATE(t.actual_trip_start_time) = ?;
    """
    
    try:
        df = pd.read_sql_query(query, conn, params=(target_date,))
    except Exception as e:
        # If the schema is incorrect or a query fails, raise it to be caught by the UI
        conn.close()
        raise e
        
    conn.close()
    return df