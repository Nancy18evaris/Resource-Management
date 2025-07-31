import streamlit as st
import sys
import os

# ✅ Add only the parent directory where all app files are stored
sys.path.append(r'M:\ResourceManagement')

# ✅ Now import all app modules correctly
import app1
import app2
import app3
import app4
import app5
import app6
import app7
import app8
import app9

# ✅ Sidebar Navigation
st.sidebar.title("📊 Industrial Workforce Analysis Dashboard")

page = st.sidebar.selectbox("Select a Page", [
    "BANKING SECTOR ANALYSIS BY STATE",
    "AVERAGE MAIN WORKERS PER STATE",
    "FEMALE WORKING RATE RURAL VS URBAN - MAIN WORKERS",
    "STATE WISE MAIN AND MARGINAL - RURAL FEMALE WORKERS ANALYSIS",
    "STATE WISE AGRICULTURE RATIO ANALYSIS",
    "FINDING IN WHICH INDUSTRY PUDUCHERRY EXCELS",
    "VISUALISATION ON WHICH INDUSTRY EACH STATE EXCELS - ANIMATED VIDEO CHART",
    "COMPARISON OF RURAL AND URBAN, MAIN AND MARGINAL WORKING WOMAN BY STATE",
    "GEOGRAPHICAL COMPARISON OF MALE VS FEMALE VS TOTAL WORKERS ACROSS INDIAN STATES"
])

# ✅ Routing each app
if page == "BANKING SECTOR ANALYSIS BY STATE":
    app1.app()

elif page == "AVERAGE MAIN WORKERS PER STATE":
    app2.app()

elif page == "FEMALE WORKING RATE RURAL VS URBAN - MAIN WORKERS":
    app3.app()

elif page == "STATE WISE MAIN AND MARGINAL - RURAL FEMALE WORKERS ANALYSIS":
    app4.app()

elif page == "STATE WISE AGRICULTURE RATIO ANALYSIS":
    app5.app()

elif page == "FINDING IN WHICH INDUSTRY PUDUCHERRY EXCELS":
    app6.app()

elif page == "VISUALISATION ON WHICH INDUSTRY EACH STATE EXCELS - ANIMATED VIDEO CHART":
    app7.app()

elif page == "COMPARISON OF RURAL AND URBAN, MAIN AND MARGINAL WORKING WOMAN BY STATE":
    app8.app()

elif page == "GEOGRAPHICAL COMPARISON OF MALE VS FEMALE VS TOTAL WORKERS ACROSS INDIAN STATES":
    app9.app()

