import logging
from string import Template
from telegram import Bot
from telegram.error import TelegramError

from .scraper import StrikeInfo 

__all__ = [
    "send_telegram_message",
    "notify_new_strike"
]

logger = logging.getLogger(__name__)

MESSAGE_TEMPLATE = Template('A new strike has been scheduled for $date. For further information: $link')


async def send_telegram_message(bot: Bot, text:str, chat_id:str) -> None:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as err:
        logger.error("Error sending Telegram message %s", err)


async def notify_new_strike(new_strikes:list[StrikeInfo], bot_token:str, chat_id:str) -> None:
    if not new_strikes:
        return
    
    async with Bot(token=bot_token) as bot:
        for strike in new_strikes:
            message = MESSAGE_TEMPLATE.substitute(date=strike.date, link=strike.link)
            await send_telegram_message(bot=bot, text=message, chat_id=chat_id)

