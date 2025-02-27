# reminders.py
import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_all_bills, get_all_users, get_last_expense_date
from config import BILL_REMINDER_DAYS, INACTIVITY_DAYS
from bot_instance import bot
from gamification import check_achievements

scheduler = BackgroundScheduler()

def check_bills():
    bills = get_all_bills()
    now = datetime.datetime.now()
    for bill in bills:
        # bill = (id, user_id, amount, category, due_date, recurrence)
        due_date_obj = datetime.datetime.strptime(bill[4], "%Y-%m-%d")
        days_left = (due_date_obj - now).days
        if 0 <= days_left <= BILL_REMINDER_DAYS:
            message = (f"Напоминание: скоро наступит срок платежа за '{bill[3]}' "
                       f"на сумму {bill[2]} сум. Срок: {bill[4]}")
            bot.send_message(bill[1], message)

def check_inactivity():
    users = get_all_users()
    now = datetime.datetime.now()
    for user_id in users:
        last_date_str = get_last_expense_date(user_id)
        if last_date_str:
            last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
            days_inactive = (now - last_date).days
            if days_inactive >= INACTIVITY_DAYS:
                playful_messages = [
                    "Ты уже несколько дней не записывал расходы! Может, пора проверить кошелек?",
                    "Эй, бюджет сам себя не контролирует — запиши траты!",
                    "Бюджет как зубная щетка – его нужно использовать регулярно!"
                ]
                bot.send_message(user_id, random.choice(playful_messages))

def check_gamification():
    users = get_all_users()
    for user_id in users:
        check_achievements(user_id)

# Планируем задачи
scheduler.add_job(check_bills, 'interval', hours=24)
scheduler.add_job(check_inactivity, 'interval', hours=24)
scheduler.add_job(check_gamification, 'interval', hours=24)

def start_scheduler():
    scheduler.start()
