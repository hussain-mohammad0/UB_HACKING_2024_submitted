import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('donation_data.db')
cursor = conn.cursor()

# Query to fetch all data from the donations table
cursor.execute('SELECT * FROM donations')

# Fetch all rows from the query result
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the connection
conn.close()
