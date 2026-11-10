# Bus strikes notifier

This project was created to send a Telegram message whenever TPL FVG (the regional public transport operator) reports a new strike, so users don't have to visit the dedicated website every time.

At the moment, it is designed for personal use, but in the future it may be integrated into a public channel or used by more users.

## Features

`scraper.py` implements these features:
- Automatic data extraction from [here](https://tplfvg.it/it/servizi/scioperi/)
- Data modeling using immutable dataclasses
- Filtering of duplicates using sets
- Saving historical data to a local JSON file
- Handling of HTTP timeouts and connection errors
- Automated message delivery via Telegram

## Requirements

//todo

## Usage

//todo

## Future developments

The next objectives are:
- Execution automation via scheduled tasks or cloud resources
- Extension of functionality to make the bot accessible and configurable by other users
