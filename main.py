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

    
# (key in the parsed dict, column width in characters)
COLUMNS = [
    ("name", 32),
    ("capital", 18),
    ("region", 10),
    ("population", 14),
    ("area", 12),
    ("languages", 24),
]


# Table layout: one entry per column, in the order they should appear.
# Each entry is (dict key to read from a parsed country, column width in
# characters). Widths are chosen by hand to fit typical values.
TABLE_COLUMNS = [
    ("name", 32),
    ("capital", 18),
    ("region", 10),
    ("population", 14),
    ("area", 12),
    ("languages", 24),
]


def display_table(countries):
    """Print a list of parsed country dicts as an aligned text table.

    The header and every row are built from TABLE_COLUMNS, so they always
    have the same columns in the same order with the same widths.
    """
    # Header: each key becomes a title ("name" -> "Name") padded to its
    # column width, then all titles are joined into one line.
    header_line = "".join(
        f"{field_name.title():<{column_width}}"
        for field_name, column_width in TABLE_COLUMNS
    )
    print(header_line)
    print("-" * len(header_line))  # underline as wide as the header

    # One row per country, built column by column.
    for country in countries:
        row_line = ""
        for field_name, column_width in TABLE_COLUMNS:
            cell_value = country[field_name]

            # Numbers (population, area) get thousands separators,
            # e.g. 83240525 -> "83,240,525". Everything else is just str().
            if isinstance(cell_value, int):
                cell_text = f"{cell_value:,}"
            else:
                cell_text = str(cell_value)

            # Trim to one less than the width so a long value can't push
            # the next column over, then pad to exactly the width.
            cell_text = cell_text[:column_width - 1]
            row_line += f"{cell_text:<{column_width}}"

        print(row_line)

def main():
    countries = get_country()
    if countries:
        display_table(countries)

if __name__ == "__main__":
    main()
