import json
import logging
from dataclasses import asdict
from pathlib import Path

from .scraper import StrikeInfo

__all__ = [
    "load_saved_strikes",
    "save_strikes",
    "filter_and_save_new_strikes"
]

logger = logging.getLogger(__name__)

DEFAULT_ARCHIVE_PATH = Path(__file__).with_name("tplstrikes.json")


def load_saved_strikes(file_path: Path = DEFAULT_ARCHIVE_PATH) -> list[StrikeInfo]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
            return [StrikeInfo(**item) for item in raw_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as err:
        logger.error("Error loading saved strikes %s", err)
        return []


def save_strikes(strikes: list[StrikeInfo], file_path: Path = DEFAULT_ARCHIVE_PATH) -> None:
    data_to_save = [asdict(strike) for strike in strikes]
    with open(file_path , "w", encoding="utf-8") as file:
        json.dump(data_to_save, file, indent=4)


def filter_and_save_new_strikes(scraped_strikes: list[StrikeInfo], file_path: Path = DEFAULT_ARCHIVE_PATH) -> list[StrikeInfo]:
    saved_strikes = load_saved_strikes(file_path)

    saved_set = set(saved_strikes)
    new_strikes = [strike for strike in scraped_strikes if strike not in saved_set]

    if new_strikes:
        saved_strikes.extend(new_strikes)
        save_strikes(saved_strikes, file_path)

    return new_strikes
