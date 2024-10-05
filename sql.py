# queries.py
import psycopg2

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    database="task_management_db",
    user="postgres",
    password="Ntbrkbl00!",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

# 1. Get all tasks for a specific user by user_id
def get_tasks_by_user(user_id):
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
    return cursor.fetchall()

# 2. Get tasks by specific status
def get_tasks_by_status(status_name):
    cursor.execute('''SELECT * FROM tasks WHERE status_id = 
                      (SELECT id FROM status WHERE name = %s);''', (status_name,))
    return cursor.fetchall()

# 3. Update a task's status
def update_task_status(task_id, new_status):
    cursor.execute('''UPDATE tasks SET status_id = 
                      (SELECT id FROM status WHERE name = %s) WHERE id = %s;''', 
                      (new_status, task_id))
    connection.commit()

# 4. Get users without tasks
def get_users_without_tasks():
    cursor.execute('''SELECT * FROM users WHERE id NOT IN 
                      (SELECT DISTINCT user_id FROM tasks);''')
    return cursor.fetchall()

# 5. Add a new task for a specific user
def add_new_task(user_id, title, description, status_name):
    cursor.execute('''INSERT INTO tasks (title, description, status_id, user_id) 
                      VALUES (%s, %s, 
                      (SELECT id FROM status WHERE name = %s), %s);''', 
                      (title, description, status_name, user_id))
    connection.commit()

# 6. Get all incomplete tasks (status not 'completed')
def get_incomplete_tasks():
    cursor.execute('''SELECT * FROM tasks WHERE status_id != 
                      (SELECT id FROM status WHERE name = 'completed');''')
    return cursor.fetchall()

# 7. Delete a specific task by id
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    connection.commit()

# 8. Find users with a specific email pattern
def find_users_by_email_pattern(pattern):
    cursor.execute("SELECT * FROM users WHERE email LIKE %s;", (pattern,))
    return cursor.fetchall()

# 9. Update a user's name
def update_user_name(user_id, new_name):
    cursor.execute("UPDATE users SET fullname = %s WHERE id = %s;", (new_name, user_id))
    connection.commit()

# 10. Get task count for each status
def get_task_count_by_status():
    cursor.execute('''SELECT status.name, COUNT(*) FROM tasks 
                      JOIN status ON tasks.status_id = status.id 
                      GROUP BY status.name;''')
    return cursor.fetchall()

# Closing the connection
cursor.close()
connection.close()
