import os
import re
import logging
from time import sleep
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_BOT = "emperor_pars_bot"     # без @
TARGET_BOT = "Nemo_Private_Bot"      # без @
EMAIL = "gosumail228@gmail.com"      # твой email

app = Application.builder().token(BOT_TOKEN).build()

def is_valid_name(name: str) -> bool:
    name = name.strip()
    if ' ' in name or len(name) <= 5:
        return False
    if not name.isalnum():
        return False
    if sum(c.isdigit() for c in name) > 4:
        return False
    return True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    # проверка, что сообщение от бота‑источника
    if msg.chat.username == SOURCE_BOT:
        text = msg.text or ""

        # парсим имя
        match = re.search(r"Имя:\\s*(\\S+)", text)
        if not match:
            return
        name = match.group(1).strip().lower()
        if not is_valid_name(name):
            return

        # парсим ссылку
        links = re.findall(r"(https?://\\S+)", text)
        if not links:
            return
        link = links[0]

        # отправляем ссылку в целевого бота
        await context.bot.send_message(chat_id=f"@{TARGET_BOT}", text=link)

        # пауза, потом email
        sleep(10)
        await context.bot.send_message(chat_id=f"@{TARGET_BOT}", text=EMAIL)

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
app.add_handler(handler)

app.run_polling()
