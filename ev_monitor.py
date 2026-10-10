import serial
from collections import deque

# Connect to Wokwi ESP32
ser = serial.serial_for_url(
    "rfc2217://localhost:4000",
    baudrate=115200,
    timeout=2
)

print("Connected to Wokwi!")
print("Waiting for ESP32 sensor data...\n")

# Store latest 5 readings
readings = deque(maxlen=5)

while True:

    # Read one line from ESP32
    line = ser.readline().decode("utf-8", errors="ignore").strip()

    if not line:
        continue

    # Split ESP32 data
    parts = line.split(",")

    # Ignore startup messages
    if len(parts) != 5:
        continue

    # Convert data
    temperature = float(parts[0])
    voltage = float(parts[1])
    current = float(parts[2])
    power = float(parts[3])
    status = parts[4]

    # Create one reading
    reading = {
        "temperature": temperature,
        "voltage": voltage,
        "current": current,
        "power": power,
        "status": status
    }

    # Add to deque
    readings.append(reading)

    print("\nNew Reading:")
    print("Temperature:", temperature, "°C")
    print("Voltage:", voltage, "V")
    print("Current:", current, "A")
    print("Power:", power, "W")
    print("ESP32 Status:", status)

    # --------------------------------
    # TEMPERATURE ANALYSIS
    # --------------------------------

    if len(readings) >= 2:

        temperatures = [
            item["temperature"]
            for item in readings
        ]

        temperature_change = (
            temperatures[-1] - temperatures[0]
        )

        print(
            "Temperature change:",
            round(temperature_change, 2),
            "°C"
        )

        if temperature_change < 5:
            temperature_trend = "STABLE"
        else:
            temperature_trend = "RISING"

        print("Temperature trend:", temperature_trend)

        if temperature < 45:
            temperature_health = "NORMAL"
        else:
            temperature_health = "ALERT"

        print("Temperature health:", temperature_health)

        # --------------------------------
        # VOLTAGE TREND
        # --------------------------------

        voltages = [
            item["voltage"]
            for item in readings
        ]

        voltage_change = (
            voltages[-1] - voltages[0]
        )

        print(
            "Voltage change:",
            round(voltage_change, 2),
            "V"
        )

        # Detect voltage trend
        if voltage_change > 5:
            voltage_trend = "RISING"

        elif voltage_change < -5:
            voltage_trend = "FALLING"

        else:
            voltage_trend = "STABLE"

        print("Voltage trend:", voltage_trend)

        # --------------------------------
        # VOLTAGE HEALTH
        # --------------------------------

        if 330 <= voltage <= 420:
            voltage_health = "NORMAL"
        else:
            voltage_health = "ALERT"

        print("Voltage health:", voltage_health)

        # --------------------------------
        # CURRENT TREND
        # --------------------------------

        currents = [
            item["current"]
            for item in readings
        ]

        current_change = (
            currents[-1] - currents[0]
        )

        print(
            "Current change:",
            round(current_change, 2),
            "A"
        )

        # Detect current trend
        if current_change > 5:
            current_trend = "RISING"

        elif current_change < -5:
            current_trend = "FALLING"

        else:
            current_trend = "STABLE"

        print("Current trend:", current_trend)
        # --------------------------------
        # CURRENT HEALTH
        # --------------------------------

        if current <= 80:
            current_health = "NORMAL"
        else:
            current_health = "ALERT"

        print("Current health:", current_health)
        # Current anomaly detection

        if len(readings) >= 5:
            recent_currents = [item["current"] for item in readings]

            average_current = sum(recent_currents) / len(recent_currents)

            current_difference = abs(current - average_current)

            if current_difference > 20:
                current_anomaly = "ANOMALY"
            else:
                current_anomaly = "NORMAL"

            print("Recent average current:",
                round(average_current, 2), "A")

            print("Current difference:",
                round(current_difference, 2), "A")

            print("Current anomaly:", current_anomaly)
            # Current min / max / average

        if len(readings) >= 5:
            recent_currents = [item["current"] for item in readings]

            minimum_current = min(recent_currents)
            maximum_current = max(recent_currents)
            average_current = sum(recent_currents) / len(recent_currents)

            print("Minimum current:", round(minimum_current, 2), "A")
            print("Maximum current:", round(maximum_current, 2), "A")
            print("Average current:", round(average_current, 2), "A")
        # --------------------------------
        # RECENT ELECTRICAL PROFILE
        # --------------------------------

        if len(readings) >= 5:

        # Temperature statistics
            recent_temperatures = [
                item["temperature"]
                for item in readings
            ]

            minimum_temperature = min(recent_temperatures)
            maximum_temperature = max(recent_temperatures)
            average_temperature = sum(recent_temperatures) / len(recent_temperatures)

            # Voltage statistics
            recent_voltages = [
                item["voltage"]
                for item in readings
            ]

            minimum_voltage = min(recent_voltages)
            maximum_voltage = max(recent_voltages)
            average_voltage = sum(recent_voltages) / len(recent_voltages)

            # Power statistics
            recent_powers = [
                item["power"]
                for item in readings
            ]

            minimum_power = min(recent_powers)
            maximum_power = max(recent_powers)
            average_power = sum(recent_powers) / len(recent_powers)

            print("\n--- Recent Electrical Profile ---")

            print(
                "Temperature:",
                round(minimum_temperature, 2),
                "-",
                round(maximum_temperature, 2),
                "°C | Avg:",
                round(average_temperature, 2),
                "°C"
            )

            print(
                "Voltage:",
                round(minimum_voltage, 2),
                "-",
                round(maximum_voltage, 2),
                "V | Avg:",
                round(average_voltage, 2),
                "V"
            )

            print(
                "Current:",
                round(minimum_current, 2),
                "-",
                round(maximum_current, 2),
                "A | Avg:",
                round(average_current, 2),
                "A"
            )

            print(
                "Power:",
                round(minimum_power, 2),
                "-",
                round(maximum_power, 2),
                "W | Avg:",
                round(average_power, 2),
                "W"
            )
        # --------------------------------
        # SEARCH FOR CURRENT OVERLOAD
        # --------------------------------

        if len(readings) >= 5:

            overload_found = False

            for item in readings:

                if item["current"] > 80:
                    overload_found = True
                    break

            if overload_found:
                print("Current overload found in recent readings: YES")
            else:
                print("Current overload found in recent readings: NO")
            # --------------------------------
        # SEARCH FOR ELECTRICAL FAULTS
        # --------------------------------

        if len(readings) >= 5:

            temperature_fault = False
            voltage_fault = False
            current_fault = False
            power_fault = False

            for item in readings:

                # Temperature fault
                if item["temperature"] >= 45:
                    temperature_fault = True

                # Voltage fault
                if item["voltage"] < 330 or item["voltage"] > 420:
                    voltage_fault = True

                # Current overload
                if item["current"] > 80:
                    current_fault = True

                # Power fault
                if item["power"] > 30000:
                    power_fault = True

            print("\n--- Recent Fault Search ---")

            print(
                "Temperature fault found:",
                "YES" if temperature_fault else "NO"
            )

            print(
                "Voltage fault found:",
                "YES" if voltage_fault else "NO"
            )

            print(
                "Current overload found:",
                "YES" if current_fault else "NO"
            )

            print(
                "Power fault found:",
                "YES" if power_fault else "NO"
            )
        # --------------------------------
        # POWER TREND
        # --------------------------------

        powers = [
            item["power"]
        for item in readings
        ]

        power_change = powers[-1] - powers[0]

        print(
            "Power change:",
            round(power_change, 2),
            "W"
        )

        # Detect power trend
        if power_change > 1000:
            power_trend = "RISING"

        elif power_change < -1000:
            power_trend = "FALLING"

        else:
            power_trend = "STABLE"

        print("Power trend:", power_trend)
        # Power health
        if power <= 30000:
            power_health = "NORMAL"
        else:
            power_health = "ALERT"

        print("Power health:", power_health)
        # Overall electrical health

        if (temperature_health == "NORMAL" and
            voltage_health == "NORMAL" and
            current_health == "NORMAL" and
            power_health == "NORMAL"):

            overall_health = "NORMAL"

        else:
            overall_health = "ALERT"

        print("Overall Electrical Health:", overall_health)