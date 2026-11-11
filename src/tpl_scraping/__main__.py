import sys
from pathlib import Path
from urllib.parse import urljoin

from dotenv import load_dotenv
import requests

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