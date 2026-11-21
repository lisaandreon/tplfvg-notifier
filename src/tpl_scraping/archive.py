import json

#json file already exists and can ben read
try:
    with open("tplstrikes.json", "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        saved_strikes = [StrikeInfo(**item) for item in raw_data]

#json file doesn't exists
except FileNotFoundError:
    saved_strikes = []

#management of duplicate data
saved_set = set(saved_strikes)
new_strikes = [strike for strike in strikes_list if strike not in saved_set]

saved_strikes.extend(new_strikes)

#json file created/updated
data_to_save = [asdict(strike) for strike in saved_strikes]
with open("tplstrikes.json", "w", encoding="utf-8") as file:
    json.dump(data_to_save, file, indent=4)

