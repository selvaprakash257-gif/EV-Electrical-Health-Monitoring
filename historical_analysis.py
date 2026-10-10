
import sqlite3

connection = sqlite3.connect("ev_health_monitor.db")
cursor = connection.cursor()

# Count stored readings
cursor.execute("SELECT COUNT(*) FROM readings")
total_readings = cursor.fetchone()[0]

print("\n--- Historical Electrical Analysis ---")
print("Total readings:", total_readings)

# Calculate maximum and average values
cursor.execute("""
    SELECT
        MAX(temperature), AVG(temperature),
        MAX(voltage), AVG(voltage),
        MAX(current), AVG(current),
        MAX(power), AVG(power)
    FROM readings
""")

result = cursor.fetchone()

print(f"Maximum temperature: {result[0]:.2f} °C")
print(f"Average temperature: {result[1]:.2f} °C")

print(f"Maximum voltage: {result[2]:.2f} V")
print(f"Average voltage: {result[3]:.2f} V")

print(f"Maximum current: {result[4]:.2f} A")
print(f"Average current: {result[5]:.2f} A")

print(f"Maximum power: {result[6]:.2f} W")
print(f"Average power: {result[7]:.2f} W")


# Count historical readings by electrical health status
cursor.execute("""
    SELECT status, COUNT(*)
    FROM readings
    GROUP BY status
""")

status_counts = cursor.fetchall()

print("\n--- Historical Health Status Report ---")

for status, count in status_counts:
    print(f"{status}: {count} readings")


# Find all historical ALERT readings
cursor.execute("""
    SELECT id, temperature, voltage, current, power, timestamp
    FROM readings
    WHERE status = 'ALERT'
    ORDER BY id DESC
""")

alerts = cursor.fetchall()

print("\n--- Historical Alert Details ---")

if alerts:
    for alert in alerts:
        print(
            f"ID: {alert[0]} | "
            f"Temperature: {alert[1]:.2f} °C | "
            f"Voltage: {alert[2]:.2f} V | "
            f"Current: {alert[3]:.2f} A | "
            f"Power: {alert[4]:.2f} W | "
            f"Time: {alert[5]}"
        )
        reasons = []

        if alert[1] >= 45:
            reasons.append("HIGH TEMPERATURE")

        if alert[2] < 330 or alert[2] > 420:
            reasons.append("VOLTAGE OUT OF RANGE")

        if alert[3] > 80:
            reasons.append("CURRENT OVERLOAD")

        if alert[4] > 30000:
            reasons.append("HIGH POWER")

        if reasons:
            print("Fault reason:", ", ".join(reasons))
        else:
            print("Fault reason: OTHER / CHECK STATUS LOGIC") 
else:
    print("No ALERT readings found.")



connection.close()
