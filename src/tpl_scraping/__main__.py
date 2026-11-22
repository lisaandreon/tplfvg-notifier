import asyncio
import logging
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

from .archive import filter_and_save_new_strikes
from .notifier import notify_new_strike
from .scraper import get_strikes

logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    load_dotenv(Path(__file__).with_name(".env"), override=True)

    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        logger.error("Telegram credentials are missing in .env file")
        sys.exit(1)


    try:
        scraped_strikes = get_strikes()
    except requests.exceptions.RequestException as err:
        logger.error("Unable to download strikes %s", err)
        sys.exit(1)


    new_strikes = filter_and_save_new_strikes(scraped_strikes)


    await notify_new_strike(
        new_strikes=new_strikes,
        bot_token=bot_token,
        chat_id=chat_id
    )


if __name__ == "__main__":
    asyncio.run(main())