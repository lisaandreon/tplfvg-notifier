import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from telegram import Bot
from telegram.error import TelegramError

load_dotenv(Path(__file__).with_name(".env"), override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

#network errors management
URL = "https://tplfvg.it/it/servizi/scioperi/"

try:
    page = requests.get(URL, timeout=10)
    page.raise_for_status()
except requests.exceptions.Timeout:
    print("Error: the request took too long.")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("Server connection error.")
    sys.exit(1)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error received from the server: {err}")
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(f"Generic network error: {err}")
    sys.exit(1)

@dataclass(frozen=True)
class StrikeInfo:
    """Class for categorize a single event"""

    date: str
    link: str

soup = BeautifulSoup(page.content, "html.parser")
strikes_box = soup.find("div", class_="w-block-cards block-cards")

strikes_list = []

#check the extracted content to avoid `AttributeError`
if strikes_box:
    bus_strikes = strikes_box.find_all("a", class_="card")

    for card in bus_strikes:
        card_date = card.find("h2", class_="card-title")

        #managing missing data
        if card_date is None: 
            continue

        card_link = card.get("href")

        strike = StrikeInfo(
            date=card_date.text.strip(),
            link=urljoin("https://tplfvg.it", card_link)
        )

        strikes_list.append(strike)

#json file already exists and can ben read
try:
    with open("tplstrikes.json", "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        saved_strikes = [StrikeInfo(**item) for item in raw_data]

#json file doesn't exists
except FileNotFoundError:
    saved_strikes = []

#management of duplicate data
saved_set = set(saved_strikes)
new_strikes = [strike for strike in strikes_list if strike not in saved_set]

#telegram bot notifying system 
async def send_telegram_message(text):
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )
    except TelegramError as err:
        print(f"Error while sending Telegram notification: {err}")

async def notify_new_strike():
    for strike in new_strikes:
        message = f"New TPL FVG strike!\nDate: {strike.date}\nLink: {strike.link}"
        await send_telegram_message(message)

#notifying system optimization
if new_strikes:
    print("Attention! New strikes found:")
    for strike in new_strikes:
        print(strike.date, "-", strike.link)
    asyncio.run(notify_new_strike())
else:
    print("Nothing new.")

saved_strikes.extend(new_strikes)

#json file created/updated
data_to_save = [asdict(strike) for strike in saved_strikes]
with open("tplstrikes.json", "w", encoding="utf-8") as file:
    json.dump(data_to_save, file, indent=4)

