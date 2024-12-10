import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Добавим администратора
cursor.execute('''
INSERT INTO users (username, password, role) VALUES (?, ?, ?)
''', ('admin', 'admin123', 'admin'))

conn.commit()
conn.close()

print("База данных создана и администратор добавлен.")
