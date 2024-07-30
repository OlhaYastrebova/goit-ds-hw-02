import sqlite3

def execute_query(sql: str, params: tuple = ()) -> list:
    """Виконує SQL-запит і повертає результати."""
    with sqlite3.connect('hw2_database') as con:
        cur = con.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

# Запит для отримання всіх завдань конкретного користувача за його user_id
def get_tasks_by_user(user_id: int) -> list:
    sql = """
    SELECT *
    FROM tasks
    WHERE user_id = ?;
    """
    return execute_query(sql, (user_id,))

# Приклад використання
user_id = 1 
tasks = get_tasks_by_user(user_id)
print(tasks)

# Запит для отримання завдань за певним статусом
def get_tasks_by_status(status_name: str) -> list:
    sql = """
    SELECT *
    FROM tasks
    WHERE status_id = (
        SELECT id
        FROM status
        WHERE name = ?
    );
    """
    return execute_query(sql, (status_name,))

# Приклад використання
status_name = 'new'  
tasks = get_tasks_by_status(status_name)
print(tasks)

# Запит для оновлення статусу конкретного завдання
def update_task_status(task_id: int, new_status: str) -> None:
    sql = """
    UPDATE tasks
    SET status_id = (
        SELECT id
        FROM status
        WHERE name = ?
    )
    WHERE id = ?;
    """
    execute_query(sql, (new_status, task_id))

# Приклад використання
task_id = 1  # Замість цього можна використовувати будь-який task_id
new_status = 'in progress'  # Замість цього можна використовувати будь-який статус
update_task_status(task_id, new_status)
print(f'Task {task_id} status updated to {new_status}')

# Запит для отримання користувачів, які не мають жодного завдання
def get_users_without_tasks() -> list:
    sql = """
    SELECT *
    FROM users
    WHERE id NOT IN (
        SELECT user_id
        FROM tasks
    );
    """
    return execute_query(sql)

# Приклад використання
users_without_tasks = get_users_without_tasks()
print(users_without_tasks)

# Запит для додавання нового завдання для конкретного користувача
def add_new_task(user_id: int, title: str, description: str, status: str) -> None:
    sql = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?);
    """
    execute_query(sql, (title, description, status, user_id))

# Приклад використання
user_id = 1  # Замість цього можна використовувати будь-який user_id
title = "New Task Title"
description = "This is the description of the new task."
status = "new"  # Замість цього можна використовувати будь-який статус

add_new_task(user_id, title, description, status)
print(f"New task added for user {user_id}")

# Запит для отримання всіх незавершених завдань
def get_incomplete_tasks() -> list:
    sql = """
    SELECT t.id, t.title, t.description, s.name as status, u.fullname as user
    FROM tasks t
    JOIN status s ON t.status_id = s.id
    JOIN users u ON t.user_id = u.id
    WHERE s.name != 'completed';
    """
    return execute_query(sql)

# Приклад використання
tasks = get_incomplete_tasks()
for task in tasks:
    print(task)

# Запит для видалення конкретного завдання за його id
def delete_task(task_id: int) -> None:
    sql = "DELETE FROM tasks WHERE id = ?;"
    execute_query(sql, (task_id,))

# Приклад використання
task_id = 22

delete_task(task_id)
print(f"Task with id {task_id} has been deleted.")