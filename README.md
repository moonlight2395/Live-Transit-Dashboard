# 🚌 Live Transit Delay Dashboard

<div align="center">
  
  ![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
  ![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
  ![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
  ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
  
  **[🔴 LIVE DEMO: Click here to explore the interactive dashboard!](https://live-transit-dashboard-kbqcqptqxt8la2bkhelk3c.streamlit.app/)**
</div>

---

## 🛑 The Core Problem: Big Data vs. Cloud Constraints
Modern public transit networks generate massive amounts of spatial and temporal telemetry data every single day. For this project, the initial challenge was processing a sprawling **40 GB relational SQLite database** containing millions of historical transit trips, schedules, and GPS coordinates across Andhra Pradesh. 

While querying this data locally is straightforward, web browsers notoriously crash when attempting to render hundreds of thousands of raw geographical points on a single map canvas. Furthermore, deploying this tool to a live, free-tier cloud environment introduced severe hardware constraints, specifically strict memory limits and a 100 MB file upload ceiling.

## 💡 The Solution
The engineering challenge was to build a full-stack dashboard that could handle enterprise-scale transit data logic, visualize complex spatial bottlenecks without browser latency, and remain lightweight enough to operate flawlessly in a constrained cloud environment. 

To solve the cloud hosting constraint, I wrote custom Python extraction scripts to slice the massive 40 GB database into a highly optimized, 1-day "Portfolio Slice." This allows the live web application to run at sub-second speeds while maintaining the exact architecture used for the enterprise-scale data.

---

## 📸 Dashboard Features



### 📊 Executive KPIs & Spatial Map Engine
To provide instant situational awareness, the dashboard opens with top-level Key Performance Indicator (KPI) cards that dynamically calculate total active trips, network-wide on-time percentages, and average system delays. Below this sits the core spatial visualization engine. Powered by **PyDeck**, the map plots transit data as interactive coordinate points layered over a clean road map. Built-in hover tooltips instantly reveal the exact location name, route ID, and real-time delay metrics for any selected transit node.
![Dashboard Preview](map.png)

### 🗄️ Dynamic Custom Database Uploader
One of the most complex features is the dynamic file uploader in the sidebar, which allows users to upload their own `.db` or `.sqlite` files directly into the live cloud environment. The backend safely caches the file, validates the internal schema to ensure the necessary tables exist, and instantly live-swaps the application's data source, transforming the dashboard into a highly flexible tool.
![Dashboard Preview](upload.png)

### 📈 Volume Analysis Plotly Graph
To complement the spatial map, I integrated a reactive **Plotly** bar chart that breaks down the raw volume of trip statuses. As the dataset changes, this graph automatically categorizes the network into clear thresholds: On-Time (<5 mins), Slight Delays (5-15 mins), and Heavy Delays (>15 mins). The chart is explicitly color-coded to perfectly match the spatial indicators on the map.
![Dashboard Preview](graph.png)

### 🎯 Reactive Filter Selection
Instead of forcing users to sift through thousands of green on-time dots to find delayed buses, the reactive state-management filter allows them to isolate specific network conditions with a single click. Selecting "Heavy Delay Only" instantly strips away the noise, recalculates the KPIs, updates the Plotly volume graph, and redraws the PyDeck map to display only the most critical transit failures.
![Dashboard Preview](filter.png)

---

## 🗺️ Project Architecture Map
Here is how the application is structured under the hood:

```text
Live-Transit-Dashboard/
│
├── app.py                 # The main Streamlit frontend & UI logic
├── database.py            # SQLite connection and backend query engine
├── extract_real_data.py   # Data engineering script (40GB -> Cloud optimized)
├── portfolio_data.db      # The lightweight, extracted dataset for the live web
├── requirements.txt       # Python library dependencies
└── assets/
    └── dashboard_preview.png  # Images for documentation
