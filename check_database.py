
import sqlite3

connection = sqlite3.connect("ev_health_monitor.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT id, temperature, voltage, current, power, status, timestamp
    FROM readings
    ORDER BY id DESC
    LIMIT 5
""")

rows = cursor.fetchall()

print("\n--- Latest 5 Stored Readings ---")

for row in rows:
    print(row)

print("\nNumber of readings displayed:", len(rows))

connection.close()
