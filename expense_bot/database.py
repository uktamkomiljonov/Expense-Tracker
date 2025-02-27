# database.py

import sqlite3
import datetime

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица для расходов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            category TEXT,
            date TEXT
        )
    ''')

    # Таблица для предстоящих платежей (биллов)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            category TEXT,
            due_date TEXT,       -- формат "YYYY-MM-DD"
            recurrence TEXT      -- например: "monthly", "yearly" или пустая строка
        )
    ''')

    # Таблица для геймификации (достижения)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_name TEXT,
            date_obtained TEXT
        )
    ''')

    conn.commit()
    conn.close()

# -- Расходы --
def add_expense(user_id, amount, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)",
                   (user_id, amount, category, date))
    conn.commit()
    conn.close()

def get_expenses(user_id, period="month"):
    """
    Возвращает все расходы за указанный период (day, week, month).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.datetime.now()

    if period == "day":
        date_filter = now.strftime("%Y-%m-%d")
        query = "SELECT * FROM expenses WHERE user_id = ? AND date = ?"
        cursor.execute(query, (user_id, date_filter))
    elif period == "week":
        week_ago = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        query = "SELECT * FROM expenses WHERE user_id = ? AND date >= ?"
        cursor.execute(query, (user_id, week_ago))
    else:  # month
        date_filter = now.strftime("%Y-%m")
        query = "SELECT * FROM expenses WHERE user_id = ? AND date LIKE ?"
        cursor.execute(query, (user_id, date_filter + "%"))

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_last_expense_date(user_id):
    """
    Возвращает дату последнего внесенного расхода.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT date FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 1"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# -- Биллы (предстоящие платежи) --
def add_bill(user_id, amount, category, due_date, recurrence):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bills (user_id, amount, category, due_date, recurrence) VALUES (?, ?, ?, ?, ?)",
                   (user_id, amount, category, due_date, recurrence))
    conn.commit()
    conn.close()

def get_all_bills():
    """
    Возвращает все биллы (для напоминаний).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM bills"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# -- Геймификация (достижения) --
def add_achievement(user_id, achievement_name):
    """
    Записываем достижение в таблицу user_achievements, если такого достижения нет.
    """
    if not has_achievement(user_id, achievement_name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        date_obtained = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO user_achievements (user_id, achievement_name, date_obtained) VALUES (?, ?, ?)",
                       (user_id, achievement_name, date_obtained))
        conn.commit()
        conn.close()

def has_achievement(user_id, achievement_name):
    """
    Проверяем, есть ли уже достижение.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT id FROM user_achievements WHERE user_id = ? AND achievement_name = ?"
    cursor.execute(query, (user_id, achievement_name))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def get_user_achievements(user_id):
    """
    Получаем список всех достижений пользователя.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT achievement_name, date_obtained FROM user_achievements WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_users():
    """
    Возвращает список уникальных user_id из таблицы расходов (или любой другой таблицы).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT DISTINCT user_id FROM expenses"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
