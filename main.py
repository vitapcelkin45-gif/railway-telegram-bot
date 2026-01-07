import os
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

SOURCE_BOT = "@emperor_pars_bot"
TARGET_BOT = "@Nemo_Private_Bot"
EMAIL_TO_SEND = "имя@gmail.com"

def is_valid_username(name):
    if " " in name or len(name) <= 5:
        return False
    digits = sum(char.isdigit() for char in name)
    return name.isalnum() and name.islower() and digits <= 4

@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def handle_message(message: types.Message):
    if message.chat.username == SOURCE_BOT.strip("@"):
        text = message.text
        name_line = next((line for line in text.splitlines() if "Имя:" in line), "")
        name = name_line.replace("Имя:", "").strip()

        if not is_valid_username(name):
            return

        if message.reply_markup:
            for row in message.reply_markup.inline_keyboard:
                for btn in row:
                    if "Объявление" in btn.text:
                        url = btn.url
                        await send_to_nemo_bot(url, name)

async def send_to_nemo_bot(url, username):
    for _ in range(5):
        await bot.send_message(TARGET_BOT, url)
        await asyncio.sleep(10)
        msgs = await bot.get_chat_history(TARGET_BOT, limit=1)
        if msgs and any(keyword in msgs[0].text for keyword in ["Обьявление спарсилось"]):
            break
    await process_gosumail()

async def process_gosumail():
    await asyncio.sleep(5)
    # Эмуляция действий: найти кнопку GosuMail, ввести почту, нажать "Отправить"
    # Здесь должен быть Telethon или пользовательский интерфейс

if __name__ == "__main__":
    executor.start_polling(dp)