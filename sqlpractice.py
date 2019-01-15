# ----Example Python Program to create tables in disk file based SQLite databases----


# Import the sqlite3 module

import sqlite3

# Create a database connection to a disk file based database

connectionObject = sqlite3.connect("weather.db")

# Obtain a cursor object

cursorObject = connectionObject.cursor()

# Drop any existing table with the same name



# Create a table in the disk file based database

createTable = "CREATE TABLE temperature(id int, temp numeric(3,1))"

cursorObject.execute(createTable)

# Insert EOD stats into the reports table

insertValues = "INSERT INTO temperature values(1,40.1)"

cursorObject.execute(insertValues)

insertValues = "INSERT INTO temperature values(2,65.4)"

cursorObject.execute(insertValues)

# Select from the temperature table

queryTable = "SELECT * from temperature"

queryResults = cursorObject.execute(queryTable)

# Print the Temperature records

print("(CityId, Temperature)")

for result in queryResults:
    print(result)

connectionObject.close()