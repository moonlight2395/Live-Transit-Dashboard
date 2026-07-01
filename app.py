import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import datetime
import os
import database

# 1. Page Configuration & Title
st.set_page_config(page_title="Transit Analytics Dashboard", layout="wide")
st.title("🚌 Live Transit Delay Dashboard")

# 2. Database Upload & Schema Instructions (Sidebar Layout)
st.sidebar.header("🗄️ Database Management")

# File uploader widget for custom SQLite files
uploaded_file = st.sidebar.file_uploader(
    "Upload custom SQLite Database", 
    type=["db", "sqlite", "sqlite3"],
    help="Upload an SQLite file conforming to the required schema guidelines."
)

# Manage the active database file path context
if uploaded_file is not None:
    # Save the uploaded file safely to a temporary local file path
    active_db_path = "portfolio_data.db"
    with open(active_db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("Using uploaded database context!")
# else:
#     active_db_path = "data.db"
#     # Clean up temp file if it exists and upload is cleared
#     if os.path.exists("temp_viewer_database.db"):
#         os.remove("temp_viewer_database.db")
#     st.sidebar.info("Using default system dataset (data.db)")
else:
    # Changed from data.db to portfolio_data.db
    active_db_path = "portfolio_data.db" 
    
    if os.path.exists("temp_viewer_database.db"):
        os.remove("temp_viewer_database.db")
        
    # Updated the sidebar text so we know it's working
    st.sidebar.info("Using portfolio dataset (portfolio_data.db)")
# Collapsible instructional manual detailing strict database expectations
with st.sidebar.expander("📝 Custom Database Requirements"):
    st.markdown("""
    To ensure your uploaded database works flawlessly, it **must contain these 3 tables** with these exact column names and formats:
    
    #### 1. Table: `trip`
    * `id` : Primary identifier for the trip.
    * `route_id` : Numeric or textual identifier for the route.
    * `start_place_id` : Connection token matching `place.place_id`.
    * `scheduled_trip_start_time` : Expected start timestamp (`YYYY-MM-DD HH:MM:SS`).
    * `actual_trip_start_time` : Realized start timestamp (`YYYY-MM-DD HH:MM:SS`).
    
    #### 2. Table: `place`
    * `place_id` : Unique ID for a transit stop.
    * `place_name` : Human-readable text label of the location.
    
    #### 3. Table: `place_coordinates`
    * `place_id` : Unique ID matching `place.place_id`.
    * `latitude` : Spatial horizontal datum coordinate (e.g., 79.xxxx).
    * `longitude` : Spatial vertical datum coordinate (e.g., 15.xxxx).
    """)

# 3. Calendar Navigation
st.sidebar.markdown("---")
st.sidebar.header("Calendar Controls")
default_date = datetime.date(2023, 10, 1)
selected_date = st.sidebar.date_input("Select Dashboard Date:", default_date)
date_str = selected_date.strftime('%Y-%m-%d')

# 4. Fetch the Data Safely
@st.cache_data(show_spinner=False)
def load_and_process_data(target_date_str, db_path):
    df_raw = database.get_daily_trips(target_date_str, db_path)
    if df_raw.empty:
        return df_raw
    
    df_raw['scheduled_start'] = pd.to_datetime(df_raw['scheduled_start'])
    df_raw['actual_start'] = pd.to_datetime(df_raw['actual_start'])
    df_raw['delay_minutes'] = (df_raw['actual_start'] - df_raw['scheduled_start']).dt.total_seconds() / 60
    df_raw['delay_minutes'] = df_raw['delay_minutes'].clip(lower=0)
    
    def assign_status(delay):
        if delay <= 5:   return "On-Time"
        if delay <= 15:  return "Slight Delay"
        return "Heavy Delay"
        
    df_raw['status'] = df_raw['delay_minutes'].apply(assign_status)
    
    def assign_color(status):
        if status == "On-Time":      return [46, 204, 113, 220]  
        if status == "Slight Delay": return [241, 196, 15, 220]  
        if status == "Heavy Delay":  return [231, 76, 60, 220]   

    df_raw['color'] = df_raw['status'].apply(assign_color)
    return df_raw

try:
    with st.spinner('Querying selected relational network database...'):
        df = load_and_process_data(date_str, active_db_path)
except Exception as error_msg:
    st.error("❌ **Database Structural Mismatch**")
    st.info("The uploaded database failed to process. Ensure all required tables (`trip`, `place`, `place_coordinates`) and target column definitions match the specification requirements inside the sidebar manual.")
    st.stop()

if df.empty:
    st.warning(f"No transit trip records discovered for the targeted matrix context on {date_str}.")
else:
    # 5. Executive KPI Cards
    total_trips = len(df)
    on_time_trips = len(df[df['status'] == "On-Time"])
    on_time_pct = (on_time_trips / total_trips) * 100 if total_trips > 0 else 0
    avg_delay = df['delay_minutes'].mean()
    heavy_delays = len(df[df['status'] == "Heavy Delay"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Trips Running", f"{total_trips:,}")
    m2.metric("Network On-Time Rate", f"{on_time_pct:.1f}%")
    m3.metric("Average System Delay", f"{avg_delay:.1f} min")
    m4.metric("Heavy Delay Alerts (>15m)", f"{heavy_delays:,}", delta_color="inverse")
    
    st.write("---")

    # 6. Map Filtering
    st.sidebar.markdown("---")
    st.sidebar.header("Filter Map View")
    view_option = st.sidebar.radio(
        "Select Trip Status to Display:",
        options=["Show All Trips", "🟢 On-Time Only", "🟡 Slight Delay Only", "🔴 Heavy Delay Only"]
    )
    
    if view_option == "Show All Trips":
        df_filtered = df
    elif "On-Time" in view_option:
        df_filtered = df[df['status'] == "On-Time"]
    elif "Slight Delay" in view_option:
        df_filtered = df[df['status'] == "Slight Delay"]
    elif "Heavy Delay" in view_option:
        df_filtered = df[df['status'] == "Heavy Delay"]

    # 7. Interactive Map Rendering
    st.subheader(f"Network Spatial Visualization ({len(df_filtered)} items on map)")
    
    if df_filtered.empty:
        st.info("No active matrix items match your sidebar selections.")
    else:
        layer = pdk.Layer(
            "ScatterplotLayer",
            df_filtered,
            get_position="[longitude, latitude]",
            get_color="color",
            get_radius=1500,        
            pickable=True,          
            auto_highlight=True     
        )

        view_state = pdk.ViewState(
            latitude=df_filtered["latitude"].mean(),
            longitude=df_filtered["longitude"].mean(),
            zoom=6.5,
            pitch=0,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="road",       
            tooltip={
                "html": """
                    <div style='font-family: Arial, sans-serif;'>
                        <b>📍 Location:</b> {place_name} <br/>
                        <b>🆔 Route ID:</b> {route_id} <br/>
                        <b>⏱️ Delay:</b> {delay_minutes:.1f} minutes <br/>
                        <b>📊 Status:</b> {status}
                    </div>
                """,
                "style": {
                    "backgroundColor": "#ffffff", 
                    "color": "#333333", 
                    "fontSize": "14px",
                    "padding": "12px",
                    "borderRadius": "8px",
                    "boxShadow": "0px 4px 6px rgba(0,0,0,0.1)"
                }
            }
        )
        st.pydeck_chart(r)

    # 8. Chart Analysis
    st.write("---")
    if not df_filtered.empty:
        status_counts = df_filtered['status'].value_counts().reset_index()
        status_counts.columns = ['Status Category', 'Total Trips']
        
        color_map = {"On-Time": "#2ecc71", "Slight Delay": "#f1c40f", "Heavy Delay": "#e74c3c"}
        
        fig = px.bar(
            status_counts, 
            x='Status Category', 
            y='Total Trips',
            color='Status Category',
            color_discrete_map=color_map,
            text='Total Trips'
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            template="plotly_white", 
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Trips",
            title={
                'text': "<b>Trip Volume Analysis</b><br><span style='font-size:13px; color:#555555;'>🟢 On-Time (<5 mins) &nbsp;&nbsp;|&nbsp;&nbsp; 🟡 Slight Delay (5-15 mins) &nbsp;&nbsp;|&nbsp;&nbsp; 🔴 Heavy Delay (>15 mins)</span>",
                'y': 0.93,
                'x': 0.0,
                'xanchor': 'left',
                'yanchor': 'top'
            },
            margin=dict(t=80)
        ) 
        st.plotly_chart(fig, use_container_width=True)