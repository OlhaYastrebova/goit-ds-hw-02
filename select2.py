import sqlite3

def execute_query(sql: str, params: tuple = ()) -> list:
    """Виконує SQL-запит і повертає результат."""
    with sqlite3.connect('hw2_database') as con:
        cur = con.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

# Запит для пошуку користувачів з певною електронною поштою
def find_users_by_email(email_pattern: str) -> list:
    sql = """
    SELECT id, fullname, email
    FROM users
    WHERE email LIKE ?;
    """
    return execute_query(sql, (email_pattern,))

# Приклад використання
email_pattern = '%example.com%'  # Шаблон для пошуку електронних адрес, що містять "example.com"

users = find_users_by_email(email_pattern)
for user in users:
    print(user)

# Запит для оновлення ім'я користувача
def update_user_fullname(user_id: int, new_fullname: str) -> None:
    sql = """
    UPDATE users
    SET fullname = ?
    WHERE id = ?;
    """
    execute_query(sql, (new_fullname, user_id))

# Приклад використання
user_id = 1  # Замініть на id користувача, якого потрібно оновити
new_fullname = "Oleg Petrov"  # Нове ім'я користувача

update_user_fullname(user_id, new_fullname)
print(f"User with id {user_id} has been updated with new fullname '{new_fullname}'.")

# Запит для отримання кількості завдань для кожного статусу
def get_task_counts_by_status() -> list:
    sql = """
    SELECT s.name as status, COUNT(t.id) as task_count
    FROM tasks t
    JOIN status s ON t.status_id = s.id
    GROUP BY s.name;
    """
    return execute_query(sql)

# Приклад використання
task_counts = get_task_counts_by_status()
for status, count in task_counts:
    print(f"Status: {status}, Task Count: {count}")

# Запит для отримання завдань, призначених користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(email_domain: str) -> list:
    sql = """
    SELECT t.id, t.title, t.description, s.name as status, u.fullname as user, u.email
    FROM tasks t
    JOIN status s ON t.status_id = s.id
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE ?;
    """
    return execute_query(sql, (email_domain,))

# Приклад використання
email_domain = '%@example.com%'  

tasks = get_tasks_by_email_domain(email_domain)
for task in tasks:
    print(task)

# Запит для отримання завдань, що не мають опису
def get_tasks_without_description() -> list:
    sql = """
    SELECT id, title, status_id, user_id
    FROM tasks
    WHERE description IS NULL OR description = '';
    """
    return execute_query(sql)

# Приклад використання
tasks_without_description = get_tasks_without_description()
for task in tasks_without_description:
    print(task)

# Запит для отримання користувачів та їхніх завдань із статусом 'in progress'
def get_users_and_tasks_in_progress() -> list:
    sql = """
    SELECT u.id as user_id, u.fullname, u.email, t.id as task_id, t.title, t.description
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    INNER JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress';
    """
    return execute_query(sql)

# Приклад використання
users_and_tasks = get_users_and_tasks_in_progress()
for user in users_and_tasks:
    print(user)

# Запит для отримання користувачів та кількості їхніх завдань
def get_users_and_task_counts() -> list:
    sql = """
    SELECT u.id as user_id, u.fullname, u.email, COUNT(t.id) as task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id, u.fullname, u.email;
    """
    return execute_query(sql)

# Приклад використання
users_and_task_counts = get_users_and_task_counts()
for user in users_and_task_counts:
    print(user)