from streamlit_autorefresh import st_autorefresh
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="EV Electrical Health Monitor",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EV Electrical Health Monitoring System")
st.caption("Electrical data from your SQLite database")
st_autorefresh(interval=2000, key="dashboard_refresh")

def get_latest_reading():
    connection = sqlite3.connect("ev_health_monitor.db")

    cursor = connection.cursor()
    cursor.execute("""
        SELECT temperature, voltage, current, power, status, timestamp
        FROM readings
        ORDER BY id DESC
        LIMIT 1
    """)

    reading = cursor.fetchone()
    connection.close()
    return reading

reading = get_latest_reading()

if reading is None:
    st.warning("No sensor readings found in the database.")
else:
    temperature, voltage, current, power, status, timestamp = reading

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Temperature", f"{temperature:.2f} °C")
    col2.metric("Voltage", f"{voltage:.2f} V")
    col3.metric("Current", f"{current:.2f} A")
    col4.metric("Power", f"{power / 1000:.2f} kW")

    st.divider()
    st.subheader("Overall Electrical Health")

    if status == "NORMAL":
        st.success(f"Status: {status}")
    else:
        st.error(f"Status: {status}")

    st.caption(f"Last stored reading: {timestamp}")
    st.info(
        "Values are taken from the latest stored database record. "
        "They update when the dashboard reruns."
    )
