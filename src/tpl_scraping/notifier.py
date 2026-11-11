from telegram import Bot
from telegram.error import TelegramError

from .scraper import StrikeInfo 

__all__ = [
    "send_telegram_message",
    "notify_new_strike"
]

async def send_telegram_message(text:str, bot_token:str, chat_id:str):
    bot = Bot(token=bot_token)  # TODO: bring this out to define bot only once
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text
        )
    except TelegramError as err:
        print(f"Error while sending Telegram notification: {err}")  # TODO: use logging instead

async def notify_new_strike(new_strikes:list[StrikeInfo], bot_token:str, chat_id:str):
    for strike in new_strikes:
        message = f"New TPL FVG strike!\nDate: {strike.date}\nLink: {strike.link}" # TODO: use template string
        await send_telegram_message(message, bot_token, chat_id)