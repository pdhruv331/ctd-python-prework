# Country Explorer CLI

Code the Dream - Python Advanced Pre-Work

## What it does

A menu-driven command-line tool for exploring country data. You can
search for a country by name or list every country in a region sorted
by population. Results print as an aligned table showing name, capital,
region, population, area, and languages. Empty input, names or regions
with no matches, and network errors all print a short message and return
you to the menu instead of crashing.

## API

[countries.dev](https://countries.dev), free and no API key required.

Endpoints used:
- `GET /countries/name/{name}` - search by name, returns a list of matches
- `GET /countries/region/{region}?sort=population` - all countries in a region

Response shape (from exploring `https://countries.dev/countries`):
1. The top-level response is a JSON list of country dicts, not a dict wrapper.
2. Fields used: `name`, `capital`, `region`, `population`, `area`, `languages`.
3. `languages` is nested: a list of dicts like `{"name": "Pashto", "iso639_1": "ps"}`.
4. Some records are missing keys entirely: 5 have no `capital`, 10 have no `area`.
   Every field is read with `.get()` and a default.

## How to run

```bash
pip install -r requirements.txt
python3 main.py
```

Then pick `1` to search by name, `2` to list a region, or `q` to quit.
