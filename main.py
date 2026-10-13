from countryapi import fetch_country, parse_countries


def get_country():
    """Prompt for a name, fetch and parse matches, return a list of dicts.

    Handles the two user-input error cases: an empty string and a name
    with no matches. Both print a message and return an empty list.
    """
    name = input("Enter a country name: ").strip()
    if not name:
        print("Please enter a name.")
        return []

    countries = parse_countries(fetch_country(name))
    if not countries:
        print(f"No country found matching '{name}'.")
    return countries

    
def main():
    for country in get_country():
        print(country)


if __name__ == "__main__":
    main()
