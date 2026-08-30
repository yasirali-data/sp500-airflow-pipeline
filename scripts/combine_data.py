import json


OLD_FILE = "stock_profiles.json"
NEW_FILE = "stock_profiles_new.json"
OUTPUT_FILE = "stock_profiles_final.json"


def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


old_data = load_json(OLD_FILE)
new_data = load_json(NEW_FILE)

combined_data = old_data + new_data

unique_data = {}
    
for company in combined_data:
    symbol = company["symbol"]
    unique_data[symbol] = company

final_data = list(unique_data.values())


with open(OUTPUT_FILE, "w") as file:
    json.dump(final_data, file, indent=4)


print(f"Total companies: {len(final_data)}")
print(f"Symbols: {[company['symbol'] for company in final_data]}")
print(f"Data saved to {OUTPUT_FILE}")