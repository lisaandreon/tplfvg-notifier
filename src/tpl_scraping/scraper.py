import os
import sys
from pathlib import Path
from urllib.parse import urljoin

from dotenv import load_dotenv
import requests

from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup


from typing import Optional

BOT_TOKEN: Optional[str] = None
CHAT_ID: Optional[str] = None


#telegram bot credentials management
load_dotenv(Path(__file__).with_name(".env"), override=True)

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

