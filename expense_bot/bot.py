# bot.py
from bot_instance import bot
from config import TOKEN
from database import init_db, add_expense, add_bill, get_expenses
from analysis import get_total_expenses, get_category_stats
from speech import recognize_voice
from advisor import generate_advice
from gamification import format_achievements
from reminders import start_scheduler

def main():
    init_db()        # Инициализируем БД
    start_scheduler() # Запускаем планировщик напоминаний
    bot.polling(none_stop=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "Привет! Я помогу тебе вести учет расходов.\n"
        "Напиши сумму и категорию, например: '10000 сум на еду'.\n"
        "Список команд:\n"
        "/add_bill — добавить платеж\n"
        "/stats — статистика расходов\n"
        "/advice — советы\n"
        "/achievements — достижения"
    )

# -- Расходы (текст) --
@bot.message_handler(func=lambda msg: msg.content_type == 'text' and not msg.text.startswith('/'))
def handle_text_expense(message):
    text = message.text.lower()
    words = text.split()
    try:
        amount = int(words[0])
        category = " ".join(words[2:]) if len(words) > 2 else "не указано"
        add_expense(message.chat.id, amount, category)
        bot.reply_to(message, f"✅ Записано: {amount} сум на {category}.")
    except ValueError:
        bot.reply_to(message, "Неверный формат. Пример: '10000 сум на еду'.")

# -- Расходы (голосовые) --
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    text = recognize_voice(bot, message)
    if text:
        message.text = text
        handle_text_expense(message)
    else:
        bot.send_message(message.chat.id, "Не удалось распознать голосовое сообщение.")

# -- Добавление билла --
@bot.message_handler(commands=['add_bill'])
def add_bill_handler(message):
    bot.send_message(message.chat.id,
        "Введи данные о платеже в формате:\n"
        "'50000 сум, коммунальные, 2025-03-01, monthly'\n"
        "где 'monthly' – периодичность (может быть пустым).")

@bot.message_handler(func=lambda msg: "," in msg.text and "сум" in msg.text)
def process_bill(message):
    try:
        parts = [p.strip() for p in message.text.split(",")]
        amount = int(parts[0].split()[0])
        category = parts[1]
        due_date = parts[2]
        recurrence = parts[3] if len(parts) > 3 else ""
        add_bill(message.chat.id, amount, category, due_date, recurrence)
        bot.reply_to(message, f"✅ Записан платеж: {amount} сум на '{category}', срок {due_date}.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# -- Статистика --
@bot.message_handler(commands=['stats'])
def send_stats(message):
    user_id = message.chat.id
    total = get_total_expenses(user_id, "month")
    stats = get_category_stats(user_id, "month")

    stats_text = "\n".join([f"{cat}: {amt} сум" for cat, amt in stats]) if stats else "Нет данных."
    bot.send_message(user_id,
        f"📊 Статистика за месяц:\n\nОбщий расход: {total} сум\n\nПо категориям:\n{stats_text}")

# -- Советы (наш алгоритм) --
@bot.message_handler(commands=['advice'])
def advice_handler(message):
    user_id = message.chat.id
    advice = generate_advice(user_id)
    bot.send_message(user_id, f"💡 Советы:\n{advice}")

# -- Достижения --
@bot.message_handler(commands=['achievements'])
def achievements_handler(message):
    user_id = message.chat.id
    text = format_achievements(user_id)
    bot.send_message(user_id, text)

if __name__ == "__main__":
    main()
