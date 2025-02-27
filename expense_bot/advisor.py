# advisor.py

from analysis import get_total_expenses, get_category_stats
from database import get_expenses
import datetime


def generate_advice(user_id):
    """
    Анализ расходов пользователя по простым правилам и возвращаем строку с советами.
    """
    # 1. Получаем общие расходы за месяц
    total_month = get_total_expenses(user_id, period="month")

    # 2. Смотрим статистику по категориям
    stats = get_category_stats(user_id, period="month")

    # 3. Собираем рекомендации
    advice_list = []

    # Пример простого правила: если общая сумма > 1 000 000 сум, предупреждаем
    if total_month > 1000000:
        advice_list.append("Ты превысил 1 000 000 сум за этот месяц. Попробуй снизить траты!")

    # Если категория "фастфуд" или "еда" занимает более 30% расходов
    sum_dict = {}
    for cat, amt in stats:
        sum_dict[cat.lower()] = amt

    if total_month > 0:
        for cat, amt in sum_dict.items():
            share = amt / total_month
            if ("еда" in cat or "фастфуд" in cat) and share > 0.3:
                advice_list.append("Много тратишь на еду вне дома. Может, чаще готовить дома?")
            if ("развлечения" in cat or "игры" in cat) and share > 0.3:
                advice_list.append(
                    "Развлечения занимают существенную часть расходов. Может, найти бесплатные варианты отдыха?")

    # Если ничего не набралось, даём общее пожелание
    if not advice_list:
        advice_list.append("Продолжай вести учет! Твои расходы выглядят сбалансированно.")

    return "\n".join(advice_list)
