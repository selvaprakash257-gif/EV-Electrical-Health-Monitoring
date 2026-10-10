
import sqlite3

# Connect to the database.
# If it doesn't exist, SQLite creates it.
connection = sqlite3.connect("ev_health_monitor.db")

# Create a cursor to execute SQL commands.
cursor = connection.cursor()

# Create a table to store sensor readings.
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    voltage REAL NOT NULL,
    current REAL NOT NULL,
    power REAL NOT NULL,
    status TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Save the database changes.
connection.commit()

# Close the connection.
connection.close()

print("Database and readings table created successfully!")
