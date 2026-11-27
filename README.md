# TPL FVG strikes notifier for Telegram

This repository contains the code for a Telegram bot I created that periodically checks the TPL FVG website for new public transport strikes and sends a notification as soon as an announcement is posted.

## Repository layout

- `src/tpl_scraping/scraper.py`: downloads the strikes page using `httpx` and extracts dates and links via `BeautifulSoup`.
- `src/tpl_scraping/archive.py`: saves the strikes that have already been seen into a JSON file to avoid duplicate notifications.
- `src/tpl_scraping/notifier.py`: formats the alert message and sends it via Telegram using `python-telegram-bot`.
- `src/tpl_scraping/main.py`: loads the environment variables and starts the scheduled control loop.
- `docker-compose.yml`: defines the container configuration, environment variables and persistent volume.

## Usage

### Environment variables

- `BOT_TOKEN` (required): Telegram bot token obtained from BotFather.
- `CHAT_ID` (required): target chat or channel ID (use the `-100` prefix for channels).
- `DATA_DIR` (optional): directory path for storing `tplstrikes.json` (defaults to `/app/data` in Docker).

### Deployment

1. Create a `.env` file in the project root with your `BOT_TOKEN` and `CHAT_ID`.
2. Run `docker compose up -d` to start the container in the background or deploy the compose file as a stack in Portainer.

### Local setup

1. Clone the repository and run `uv sync` to install dependencies.
2. Create a `.env` file inside `src/tpl_scraping/` containing `BOT_TOKEN` and `CHAT_ID`.
3. Start the bot with `uv run python -m tpl_scraping`.

## Future developments

- Integrating an LLM to process the text of each strike announcement and extract structured data like affected lines, schedules, and guaranteed service windows. This will allow the bot to send a complete summary directly on Telegram.
