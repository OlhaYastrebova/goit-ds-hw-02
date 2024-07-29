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
user_id = 1  # Замість цього можна використовувати будь-який user_id
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
status_name = 'new'  # Замість цього можна використовувати будь-який статус
tasks = get_tasks_by_status(status_name)
print(tasks)
