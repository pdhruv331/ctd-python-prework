"""Fetch and parse country data from the countries.dev API.

This module talks to the network and cleans up the raw JSON.
It never prints results; that is main.py's job.
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


def fetch_by_region(region, sort="population"):
    """Return all countries in `region`, sorted by the given field.

    Valid regions: Africa, Americas, Asia, Europe, Oceania.
    Returns an empty list on a 404 (unknown region) or network failure.
    """
    request_url = f"{BASE_URL}/region/{region.strip().lower()}"
    try:
        # `params` becomes ?sort=<sort> on the URL; requests encodes it.
        response = requests.get(request_url, params={"sort": sort}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return []
    except requests.exceptions.RequestException as err:
        print(f"Network error: {err}")
        return []


def parse_country(raw_data):
    """Flatten one raw API record into a small dict of the fields we display.

    Every lookup uses .get() with a default because some records are missing
    keys (5 have no capital, 10 have no area).
    """
    # `languages` is a list of dicts like {"name": "Pashto", ...};
    # pull out just the names, defaulting to an empty list if absent.

    languages = []
    for lang in raw_data.get("languages", []):
        languages.append(lang.get("name", ""))

    return {
        "name": raw_data.get("name", "N/A"),
        "capital": raw_data.get("capital", "N/A"),
        "region": raw_data.get("region", "N/A"),
        "population": raw_data.get("population", 0),
        "area": raw_data.get("area", 0),
        "languages": ", ".join(languages),
    }


def parse_countries(raw_list):
    """Apply parse_country to every record in the API response."""
    return [parse_country(country) for country in raw_list]