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

## 🛑 The Problem
Modern public transit networks generate massive amounts of telemetry data daily. In this project, I was tasked with analyzing a **40 GB relational database** of historical transit trips across Andhra Pradesh. 

The core challenge was two-fold:
1. **Scale:** Standard visualization tools crash when attempting to render hundreds of thousands of geographical coordinate points.
2. **Cloud Limitations:** Free-tier cloud hosting platforms restrict file sizes and memory, making it impossible to host the full 40 GB database live on the internet.

## 💡 The Solution
I engineered a full-stack, spatial analytics dashboard that allows users to instantly visualize network health, filter by delay severity, and upload their own transit datasets. 

To solve the cloud hosting constraint, I wrote custom Python extraction scripts to slice the massive 40 GB database into a highly optimized, 1-day "Portfolio Slice." This allows the live web application to run at sub-second speeds while maintaining the exact architecture used for the enterprise-scale data.

---

## 📸 Dashboard Features
*(Interactive Spatial Map, Dynamic Charting, and Custom Database Uploader)*

![Dashboard Preview](assets/dashboard_preview.png)

### Core Capabilities:
* **Spatial Mapping:** Renders vast arrays of geographical coordinates without browser lag using PyDeck.
* **Reactive Data Engine:** Built on an optimized SQLite database backend for instant metric recalculations.
* **Custom User Uploads:** A dynamic UI component allowing users to upload their own `.db` files directly to the cloud interface.
* **KPI Tracking:** Real-time calculation of overall network on-time percentage and average system delays.

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
    └── dashboard.png      # Images for documentation
