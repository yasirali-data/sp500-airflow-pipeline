SELECTED_SYMBOLS = [
    "MMM",
    "AOS",
    "ABT",
    "ABBV",
    "ACN",
    "ADBE"
]


def get_sp500_symbols():
    return SELECTED_SYMBOLS


if __name__ == "__main__":
    symbols = get_sp500_symbols()

    print(f"Selected symbols: {len(symbols)}")
    print(symbols)