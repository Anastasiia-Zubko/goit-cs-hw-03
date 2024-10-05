# seed.py
from faker import Faker
import psycopg2

# Initialize Faker instance
fake = Faker()

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    database="task_management_db",
    user="postgres",
    password="Ntbrkbl00!",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

# Insert statuses into the status table
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;", (status,))

# Insert fake data into the users and tasks table
for _ in range(10):
    fullname = fake.name()
    email = fake.email()

    # Insert user and get user ID
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
    user_id = cursor.fetchone()[0]

    # Insert tasks for each user
    for _ in range(3):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status_id = fake.random_element([1, 2, 3])  # Status reference
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
            (title, description, status_id, user_id)
        )

# Commit the transaction and close connection
connection.commit()
cursor.close()
connection.close()

print("Data seeded successfully!")
