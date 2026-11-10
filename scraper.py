import asyncio
import json
import os
from pathlib import Path
from urllib.parse import urljoin
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from telegram import Bot

@dataclass
class StrikeInfo:
    """Class for categorize a single event"""
    date: str
    link: str
    
load_dotenv(Path(__file__).with_name(".env"), override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

URL = "https://tplfvg.it/it/servizi/scioperi/"
page = requests.get(URL)
page.raise_for_status() #rising an exception when server returns http error

soup = BeautifulSoup(page.content, "html.parser")

strikes_box = soup.find("div", class_="w-block-cards block-cards")
bus_strikes = strikes_box.find_all("a", class_="card")

strikes_list = []

for card in bus_strikes:
    card_date = card.find("h2", class_="card-title")

    #managing missing data
    if card_date is None: 
        continue

    card_link = card.get("href")

    strike = StrikeInfo(
        date=card_date.text,
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

#new empty set
saved_id = set()

for strike in saved_strikes:
    strike_id = (strike.date, strike.link)
    saved_id.add(strike_id)

new_strikes = []

for strike in strikes_list:
    strike_id = (strike.date, strike.link)

    if strike_id not in saved_id:
        new_strikes.append(strike)

if new_strikes:
    print("Attention! New strikes found:")
    for strike in new_strikes:
        print(strike.date, "-", strike.link)
else:
    print("Nothing new.")

saved_strikes.extend(new_strikes)

#telegram bot notifying system 
async def send_telegram_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )

async def notify_new_strike():
    for strike in new_strikes:
        message = f"New TPL FVG strike!\nDate: {strike['date']}\nLink: {strike['link']}"
        await send_telegram_message(message)

asyncio.run(notify_new_strike())

#json file created/updated
data_to_save = [asdict(strike) for strike in saved_strikes]
with open("tplstrikes.json", "w", encoding="utf-8") as file:
    json.dump(data_to_save, file, indent=4)

