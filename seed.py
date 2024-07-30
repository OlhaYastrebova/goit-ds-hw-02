import faker
from random import randint
import sqlite3

NUMBER_USERS = 10
NUMBER_STATUSES = 3
NUMBER_TASKS = 30

def generate_fake_data(number_users, number_statuses, number_tasks) -> tuple:
    fake_users = []
    fake_statuses = []
    fake_tasks = []
    fake_data = faker.Faker()

    # Генерація користувачів
    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))

    # Генерація статусів
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        fake_statuses.append((status,))

    # Генерація завдань
    for _ in range(number_tasks):
        fake_tasks.append((fake_data.sentence(), fake_data.text(), randint(1, number_statuses), randint(1, number_users)))

    return fake_users, fake_statuses, fake_tasks

def insert_data_to_db(users, statuses, tasks) -> None:
    with sqlite3.connect('hw2_database') as con:
        cur = con.cursor()

        # Вставка статусів
        sql_to_statuses = """INSERT INTO status(name) VALUES (?)"""
        cur.executemany(sql_to_statuses, statuses)

        # Вставка користувачів
        sql_to_users = """INSERT INTO users(fullname, email) VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        # Вставка завдань
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        con.commit()

if __name__ == "__main__":
    users, statuses, tasks = generate_fake_data(NUMBER_USERS, NUMBER_STATUSES, NUMBER_TASKS)
    insert_data_to_db(users, statuses, tasks)
