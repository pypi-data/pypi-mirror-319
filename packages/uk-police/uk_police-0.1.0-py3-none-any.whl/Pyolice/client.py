import requests
from .exceptions import APIError

class uk_police:
    BASE_URL = "https://data.police.uk/api"

    def __init__(self):
        pass

    def _get(self, endpoint: str, params: dict = None):
        """Send a GET request to the UK Police API."""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")
