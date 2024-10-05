# create_tables.py
import psycopg2

# Establish a database connection
connection = psycopg2.connect(
    database="task_management_db",
    user="postgres",
    password="Ntbrkbl00!",
    host="localhost",
    port="5432"
)

# Create a cursor object
cursor = connection.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
''')

# Create the status table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
''')

# Create the tasks table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
''')

# Commit the transaction and close connection
connection.commit()
cursor.close()
connection.close()

print("Tables created successfully!")
