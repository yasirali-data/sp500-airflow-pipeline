import os
import json
import requests


FMP_API_URL = "https://financialmodelingprep.com/stable/profile"

# Task 2: exactly 2 FMP API calls
SYMBOLS_TO_FETCH = [
    "ABT",
    "ABBV",
]

OUTPUT_FILE = "stock_profiles_final.json"


def get_company_profile(symbol):
    api_key = os.getenv("FMP_API_KEY")

    if not api_key:
        raise ValueError(
            "FMP_API_KEY environment variable is not set"
        )

    params = {
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(
        FMP_API_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def fetch_profiles():
    print(f"Symbols to fetch: {SYMBOLS_TO_FETCH}")

    all_data = []

    for symbol in SYMBOLS_TO_FETCH:
        print(f"Fetching {symbol}...")

        data = get_company_profile(symbol)

        if data:
            all_data.extend(data)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(all_data, file, indent=4)

    print(
        f"Successfully fetched {len(SYMBOLS_TO_FETCH)} companies"
    )
    print(f"Data saved to {OUTPUT_FILE}")

    return all_data


if __name__ == "__main__":
    fetch_profiles()
