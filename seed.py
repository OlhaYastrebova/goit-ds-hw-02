from datetime import datetime
import faker
from random import randint, choice
import sqlite3

# Кількість даних для генерації
NUMBER_USERS = 10
NUMBER_TASKS = 20

def generate_fake_data(number_users, number_tasks) -> tuple:
    fake_users = []  # тут зберігатимемо користувачів
    fake_statuses = ['new', 'in progress', 'completed']  # статуси
    fake_data = faker.Faker()
    
    # Генерація користувачів
    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))
    
    return fake_users, fake_statuses

def seed_database():
    # Параметри бази даних
    DB_NAME = 'hw2_database'
    
    # Підключення до бази даних
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Отримання згенерованих даних
    fake_users, fake_statuses = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    
    # Очищення таблиці status перед заповненням новими даними
    cursor.execute('DELETE FROM status')
    
    # Заповнення таблиці status
    cursor.executemany(
        'INSERT INTO status (name) VALUES (?)',
        [(status,) for status in fake_statuses]
    )
    
    # Заповнення таблиці users
    cursor.executemany(
        'INSERT INTO users (fullname, email) VALUES (?, ?)',
        fake_users
    )
    
    # Отримання id з таблиць для tasks
    cursor.execute('SELECT id FROM status')
    status_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]
    
    # Генерація завдань
    fake_data = faker.Faker()
    fake_tasks = [
        (
            fake_data.sentence(),  # title
            fake_data.text(),      # description
            choice(status_ids),    # status_id
            choice(user_ids)       # user_id
        )
        for _ in range(NUMBER_TASKS)
    ]
    
    # Заповнення таблиці tasks
    cursor.executemany(
        'INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)',
        fake_tasks
    )
    
    # Підтвердження змін
    conn.commit()
    
    # Закриття з'єднання
    conn.close()
    print('Database seeded successfully!')

# Запуск функції для заповнення бази даних
seed_database()
