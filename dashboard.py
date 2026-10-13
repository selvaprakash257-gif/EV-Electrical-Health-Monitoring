
import sqlite3
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

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


def get_historical_readings():
    connection = sqlite3.connect("ev_health_monitor.db")

    query = """
        SELECT timestamp, temperature, voltage, current, power
        FROM (
            SELECT id, timestamp, temperature, voltage, current, power
            FROM readings
            ORDER BY id DESC
            LIMIT 10
        )
        ORDER BY id ASC
    """

    dataframe = pd.read_sql_query(query, connection)
    connection.close()

    return dataframe


# Latest electrical reading
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
        st.success("NORMAL — All monitored values are within the configured limits.")
    else:
        st.error("ALERT — One or more electrical readings need attention.")

        reasons = []

        if temperature >= 45:
            reasons.append(
                "High temperature: The temperature is above the "
                "configured limit. Check the sensor and cooling system."
            )

        if voltage < 330:
            reasons.append(
                "Low voltage: The voltage is below 330 V. "
                "Check the power supply and voltage sensor."
            )
        elif voltage > 420:
            reasons.append(
                "High voltage: The voltage is above 420 V. "
                "Check the power supply and voltage sensor."
            )

        if current > 80:
            reasons.append(
                "High current: The current is above 80 A. "
                "Check the electrical load and current sensor."
            )

        if power > 30000:
            reasons.append(
                "High power: The measured power is above 30 kW. "
                "Check the voltage and current readings."
            )

        if reasons:
            st.markdown("**What needs attention?**")
            for reason in reasons:
                st.warning(reason)
        else:
            st.info(
                "The system reported an alert, but the cause was not "
                "identified by these checks. Verify the sensor readings."
            )

    st.caption(f"Last stored reading: {timestamp}")
    st.info(
        "Values come from the latest stored database record "
        "and update automatically."
    )



# Historical electrical graphs
st.divider()
st.header("📈 Historical Electrical Data")

history = get_historical_readings()

if history.empty:
    st.warning("No historical readings available yet.")
else:
    history["timestamp"] = pd.to_datetime(history["timestamp"])
    history["time"] = history["timestamp"].dt.strftime("%H:%M:%S")

    chart_data = history.set_index("time")

    st.subheader("🌡️ Battery Temperature (°C)")
    st.line_chart(chart_data[["temperature"]])

    st.subheader("⚡ Battery Voltage (V)")
    st.line_chart(chart_data[["voltage"]])

    st.subheader("🔌 Battery Current (A)")
    st.line_chart(chart_data[["current"]])

    st.subheader("📊 Electrical Power (W)")
    st.line_chart(chart_data[["power"]])

