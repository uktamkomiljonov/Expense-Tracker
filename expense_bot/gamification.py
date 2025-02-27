# gamification.py

import datetime
from database import add_achievement, has_achievement, get_user_achievements
from analysis import get_total_expenses


def check_achievements(user_id):
    """
    Проверяем, есть ли новые достижения, и если да, добавляем их.
    """
    # 1. "7 дней подряд" - упрощённо
    # Для этого надо проверить, есть ли записи расходов за последние 7 дней
    # и нет пропусков. Для простоты покажем идею:
    # (В реальности нужно анализировать каждую дату, но тут упрощённо)

    # 2. "Снизил траты на 10% по сравнению с прошлым месяцем"
    # month - текущий месяц, prev_month - предыдущий месяц

    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")
    prev_month_date = (now.replace(day=1) - datetime.timedelta(days=1))
    prev_month = prev_month_date.strftime("%Y-%m")

    current_total = get_total_expenses(user_id, period="month")  # За текущий месяц
    # Для предыдущего месяца сделаем небольшую функцию:
    prev_total = _get_total_expenses_prev_month(user_id, prev_month)

    # Если предыдущий месяц есть и пользователь снизил траты на 10%
    if prev_total > 0:
        decrease = (prev_total - current_total) / prev_total
        if decrease >= 0.1:
            # Присваиваем достижение "Frugal Hero"
            add_achievement(user_id, "Frugal Hero")


def _get_total_expenses_prev_month(user_id, prev_month):
    """
    Считаем сумму расходов за указанный месяц (например, '2025-01').
    """
    import sqlite3
    from database import DB_NAME
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date LIKE ?"
    cursor.execute(query, (user_id, prev_month + "%"))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0


def format_achievements(user_id):
    """
    Возвращаем красиво отформатированный список достижений.
    """
    achievements = get_user_achievements(user_id)
    if not achievements:
        return "У тебя пока нет достижений. Продолжай вести учет!"

    text = "Твои достижения:\n"
    for name, date_obtained in achievements:
        text += f" - {name} (получено {date_obtained})\n"
    return text
