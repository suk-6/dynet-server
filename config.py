import os
from dotenv import load_dotenv

load_dotenv()


ENDPOINT = os.getenv("ENDPOINT")
ALLOWEDIPS = os.getenv("ALLOWEDIPS")
DNS = os.getenv("DNS")
