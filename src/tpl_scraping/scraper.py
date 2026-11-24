import logging
from dataclasses import dataclass
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

__all__ = [
    "StrikeInfo",
    "fetch_strikes_page",
    "parse_strikes",
    "get_strikes"
]

logger = logging.getLogger(__name__)

BASE_URL = "https://tplfvg.it"
STRIKES_URL = "https://tplfvg.it/it/servizi/scioperi/"


@dataclass(frozen=True)
class StrikeInfo:
    """Class for categorize a single event"""
    date: str
    link: str


def fetch_strikes_page(url: str = STRIKES_URL) -> bytes:
    logger.info("Fetching strikes page from %s", url)
    page = httpx.get(url, follow_redirects=True, timeout=10)
    page.raise_for_status()
    logger.info("Response received with status %s", page.status_code)
    return page.content


def parse_strikes(html_content: bytes) -> list[StrikeInfo]:
    soup = BeautifulSoup(html_content, "html.parser")
    strikes_box = soup.find("div", class_="w-block-cards block-cards")

    if not strikes_box:
        return []
    
    strikes_list: list[StrikeInfo] = []

    bus_strikes = strikes_box.find_all("a", class_="card")

    for card in bus_strikes:
        card_date = card.find("h2", class_="card-title")

        #managing missing data
        if card_date is None: 
            continue

        card_link = card.get("href")
        
        if not isinstance(card_link, str):
            continue

        strike = StrikeInfo(
            date=card_date.text.strip(),
            link=urljoin(BASE_URL, card_link)
        )

        strikes_list.append(strike)

    return strikes_list


def get_strikes() -> list[StrikeInfo]:
    try:
        html_content = fetch_strikes_page()
    except httpx.HTTPError as err:
        logger.error("Error fetching strikes page %s", err)
        return []
    return parse_strikes(html_content)

