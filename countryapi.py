"""Fetch and parse country data from the countries.dev API.

This module talks to the network and cleans up the raw JSON.
It never prints results; that is display.py's job.
"""

import requests

# All endpoints hang off this root. The name search is BASE_URL/name/{name}.
BASE_URL = "https://countries.dev/countries"


def fetch_country(name):
    """Search the API for countries matching `name`.

    Returns a list of raw country dicts (the API returns a list even for
    a single match). Returns an empty list on a 404 (no match) or on any
    network failure so the caller never has to deal with an exception.
    """
    # strip() guards against trailing spaces; lower() keeps the URL consistent.
    request_url = f"{BASE_URL}/name/{name.strip().lower()}"
    try:
        # timeout stops the program hanging forever if the API is slow.
        response = requests.get(request_url, timeout=10)
        # Turns 4xx/5xx status codes into an HTTPError we can catch below.
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        # The API answers 404 "Country not found" for an unknown name.
        return []
    except requests.exceptions.RequestException as err:
        # Covers DNS failure, no internet, timeouts, etc.
        print(f"Network error: {err}")
        return []

print(fetch_country("united states of america"))