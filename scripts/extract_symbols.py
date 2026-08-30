import pandas as pd
import requests
from io import StringIO

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_sp500_symbols():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; SP500-Airflow-Pipeline/1.0)"
    }

    response = requests.get(
        WIKIPEDIA_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))

    sp500_df = tables[0]

    symbols = sp500_df["Symbol"].tolist()

    return symbols


if __name__ == "__main__":
    symbols = get_sp500_symbols()

    print(f"Total symbols: {len(symbols)}")
    print(symbols[:10])
