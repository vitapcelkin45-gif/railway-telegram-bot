import os
import re
import time
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_BOT = "emperor_pars_bot"  # без @
TARGET_BOT = "Nemo_Private_Bot"   # без @
EMAIL = "gosumail228@gmail.com"   # жёстко заданный email

# Создаём приложение
app = ApplicationBuilder().token(BOT_TOKEN).build()

def is_valid_name(name: str) -> bool:
    name = name.strip()
    if ' ' in name or len(name) <= 5:
        return False
    if not name.isalnum():
        return False
    if sum(c.isdigit() for c in name) > 4:
        return False
    return True

async def handle_message(update: Update, context: CallbackContext):
    msg = update.message
    if not msg:
        return

    if msg.chat.username == SOURCE_BOT:
        text = msg.text or ""

        # Парсим имя
        m = re.search(r"Имя: (.+?)\\s+Chat", text)
        if not m:
            return
        name = m.group(1).strip()
        if not is_valid_name(name.lower()):
            return

        # Парсим ссылку
        links = re.findall(r"(https?://\S+)", text)
        if not links:
            return

        link = links[0]

        # Отправляем ссылку целевому боту
        await context.bot.send_message(chat_id=f"@{TARGET_BOT}", text=link)
        time.sleep(10)  # ждём 10 секунд
        await context.bot.send_message(chat_id=f"@{TARGET_BOT}", text=EMAIL)

# Добавляем хендлер
handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
app.add_handler(handler)

# Запускаем бота
app.run_polling()
