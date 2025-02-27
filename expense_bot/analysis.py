# analysis.py

import sqlite3
import datetime
from database import DB_NAME

def get_total_expenses(user_id, period="month"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.datetime.now()

    if period == "day":
        date_filter = now.strftime("%Y-%m-%d")
        query = "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date = ?"
        cursor.execute(query, (user_id, date_filter))
    elif period == "week":
        week_ago = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        query = "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date >= ?"
        cursor.execute(query, (user_id, week_ago))
    else:  # month
        date_filter = now.strftime("%Y-%m")
        query = "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date LIKE ?"
        cursor.execute(query, (user_id, date_filter + "%"))

    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def get_category_stats(user_id, period="month"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.datetime.now()

    if period == "day":
        date_filter = now.strftime("%Y-%m-%d")
        query = "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date = ? GROUP BY category"
        cursor.execute(query, (user_id, date_filter))
    elif period == "week":
        week_ago = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        query = "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date >= ? GROUP BY category"
        cursor.execute(query, (user_id, week_ago))
    else:  # month
        date_filter = now.strftime("%Y-%m")
        query = "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date LIKE ? GROUP BY category"
        cursor.execute(query, (user_id, date_filter + "%"))

    stats = cursor.fetchall()
    conn.close()
    return stats if stats else []
