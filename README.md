# EV Electrical Health Monitoring System

## Project Overview

The **EV Electrical Health Monitoring System** is a prototype designed to monitor important electrical parameters of an Electric Vehicle (EV) battery system. It collects simulated sensor readings, analyzes electrical conditions, stores historical data, and displays the results on a live dashboard.

The system helps identify abnormal temperature, voltage, current, and power readings and explains detected issues in simple English.

## Objectives

- Monitor battery temperature, voltage, current, and power.
- Identify abnormal electrical readings using configured thresholds.
- Display the overall electrical health status.
- Store sensor readings in an SQLite database.
- Visualize recent historical readings using graphs.
- Explain detected alerts in simple, understandable English.

## Technologies Used

- **Hardware simulation:** ESP32 and Wokwi
- **Programming language:** Python
- **Embedded programming:** Arduino C++
- **Database:** SQLite
- **Dashboard:** Streamlit
- **Data analysis:** Pandas
- **Sensor simulation:** DS18B20 and potentiometers
- **Version control:** Git and GitHub

## System Architecture

Wokwi ESP32 Simulation → Python Monitoring System → SQLite Database → Streamlit Dashboard

The ESP32 sends simulated sensor readings over a serial connection. Python processes the readings and stores valid measurements in SQLite. The Streamlit dashboard displays the latest readings, electrical health status, fault explanations, and historical graphs.

## Monitored Parameters

| Parameter | Unit | Demonstration Threshold |
|---|---|---|
| Temperature | °C | Alert at 45°C or above |
| Voltage | V | Expected range: 330–420 V |
| Current | A | Alert above 80 A |
| Power | W | Alert above 30,000 W |

These are prototype demonstration thresholds, not universal EV battery safety limits.

## Main Features

- Live electrical parameter monitoring
- Automatic storage of readings in SQLite
- Historical electrical analysis
- Temperature, voltage, current, and power graphs
- Basic sensor-reading validation
- Electrical health status detection
- Simple-English fault explanations

## How to Run

### 1. Requirements

Install Python and the required packages:

```bash
python -m pip install streamlit pandas streamlit-autorefresh pyserial
```

Install the Arduino CLI, ESP32 board support, and the required Arduino libraries: OneWire and DallasTemperature.

### 2. Prepare the ESP32 simulation

Open the project in VS Code with Wokwi configured. Compile the ESP32 sketch and start the Wokwi simulation so its RFC2217 serial server is available.

### 3. Start the Python monitoring system

Open a terminal in the project folder and run:

```bash
python ev_monitor.py
```

Keep this terminal running while monitoring sensor readings.

### 4. Start the dashboard

Open a second terminal in the same project folder and run:

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

Keep Wokwi, the Python monitor, and Streamlit running for live updates.

## Limitations

- Sensor inputs are simulated in Wokwi; this is not a production EV battery management system.
- The configured thresholds are for demonstration and require engineering validation before use with real hardware.
- Historical graphs display a limited number of recent database readings.
- Physical implementation requires appropriate voltage/current sensing, isolation, protection, and safe signal conditioning.

## Future Improvements

Physical sensor integration and additional features may be considered if time and resources permit.

## Author

Selva Prakash

GitHub: EV Electrical Health Monitoring System