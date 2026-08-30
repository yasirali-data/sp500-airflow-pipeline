# import os
# import json
# import requests


# FMP_API_URL = "https://financialmodelingprep.com/stable/profile"


# def get_company_profile(symbol):
#     api_key = os.getenv("FMP_API_KEY")

#     if not api_key:
#         raise ValueError("FMP_API_KEY environment variable is not set")

#     params = {
#         "symbol": symbol,
#         "apikey": api_key
#     }

#     response = requests.get(
#         FMP_API_URL,
#         params=params,
#         timeout=30
#     )

#     response.raise_for_status()

#     return response.json()


# if __name__ == "__main__":

#     symbols = ["MMM", "AOS"]

#     all_data = []

#     for symbol in symbols:

#         data = get_company_profile(symbol)

#         all_data.extend(data)

#     with open("stock_profiles.json", "w") as file:
#         json.dump(all_data, file, indent=4)

#     print("Data successfully saved to stock_profiles.json")



















import os
import json
import requests

from extract_symbols import get_sp500_symbols


FMP_API_URL = "https://financialmodelingprep.com/stable/profile"


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

    symbols = ["MMM", "AOS", "ABT", "ABBV", "ACN"]

    all_data = []

    for symbol in symbols:
        print(f"Fetching {symbol}...")

        data = get_company_profile(symbol)

        all_data.extend(data)


    with open("stock_profiles.json", "w") as file:
        json.dump(all_data, file, indent=4)

    print(f"Data successfully saved to stock_profiles.json")
    print(f"Total profiles: {len(all_data)}")
