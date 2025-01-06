import re
import json
import unicodedata
from discord_webhook import DiscordWebhook

with open("source/Pokemon", "r", encoding="utf8") as file:
    pokemon_list = file.read()


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    return re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)


def read_config(filename="Source/Config.json"):
    with open(filename, "r") as f:
        return json.load(f)


def send_log(embed, WEBHOOK_URL):
    webhook = DiscordWebhook(url=WEBHOOK_URL, username="Pokefier Log")
    webhook.add_embed(embed)
    webhook.execute()


def extract_pokemon_data(text):
    pattern = r"Level (\d+) ([^(]+) \(([\d.]+)%\)[.!]*"  # Pattern To Extract Level, Name, And IV
    match = re.search(pattern, text)

    if match:
        level = match.group(1)
        name = match.group(2).strip()

        name = re.sub(r"<:[^>]+>", "", name)  # If Emoji, Remove It

        iv = match.group(3)
        return {"level": level, "name": name.strip(), "IV": iv}

    else:
        return None


def load_pokemon_data():
    with open("Source/Data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def remove_diacritics(input_str):
    normalized_str = unicodedata.normalize("NFD", input_str)
    ascii_str = "".join(c for c in normalized_str if unicodedata.category(c) != "Mn")
    return ascii_str
