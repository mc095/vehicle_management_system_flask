from flask import Flask
import sqlite3

app = Flask(__name__)

# Connect to SQLite
conn = sqlite3.connect('vehicles.db')  # SQLite uses a file-based database

cursor = conn.cursor()

# Create the users_list table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_list (
        sno INTEGER PRIMARY KEY AUTOINCREMENT,
        userID TEXT,
        password TEXT,
        email TEXT,
        city TEXT,
        phone_number TEXT
    )
''')

# Create the vehicle_list table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicle_list (
        vehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicleName VARCHAR(40),
        vehicleType VARCHAR(40),
        licenseNumber VARCHAR(40),
        seatingCapacity INT,
        purchaseDate DATE
    )
''')

# Commit the changes
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("users_list and vehicle_list tables created successfully.")
