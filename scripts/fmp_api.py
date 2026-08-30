import os
import json
import requests

from extract_symbols import get_sp500_symbols


FMP_API_URL = "https://financialmodelingprep.com/stable/profile"

ALREADY_FETCHED = {"MMM", "AOS"}


def get_company_profile(symbol):
    api_key = os.getenv("FMP_API_KEY")

    if not api_key:
        raise ValueError("FMP_API_KEY environment variable is not set")

    params = {
        "symbol": symbol,
        "apikey": api_key
    }

    response = requests.get(
        FMP_API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    symbols = get_sp500_symbols()

    symbols_to_fetch = [
        symbol for symbol in symbols
        if symbol not in ALREADY_FETCHED
    ]

    print(f"Symbols to fetch: {symbols_to_fetch}")

    all_data = []

    for symbol in symbols_to_fetch:
        print(f"Fetching {symbol}...")

        data = get_company_profile(symbol)

        if data:
            all_data.extend(data)

    with open("stock_profiles_new.json", "w") as file:
        json.dump(all_data, file, indent=4)

    print(
        f"Successfully fetched {len(symbols_to_fetch)} companies"
    )
    print("Data saved to stock_profiles_new.json")