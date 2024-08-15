import re
import json
import unicodedata
import humanfriendly
from discord_webhook import DiscordWebhook


def read_config(filename="Source/Config.json"):

    with open(filename, "r") as f:
        return json.load(f)


def send_log(embed, WEBHOOK_URL):

    webhook = DiscordWebhook(url=WEBHOOK_URL, username="Pokefier Log")
    webhook.add_embed(embed)
    webhook.execute()


def is_spawn_message(message, whitelisted_channels, POKETWO_ID):

    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and len(message.embeds) > 0
        and "wild pokémon has appeared".lower() in message.embeds[0].title.lower()
    )


def is_captcha_message(message, whitelisted_channels, id, POKETWO_ID):

    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and f"https://verify.poketwo.net/captcha/{id}" in message.content
    )


def is_pokemon_caught_message(message, whitelisted_channels, id, POKETWO_ID):

    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and f"<@{id}>" in message.content
        and "you caught a level" in message.content.lower()
    )

def is_pokemon_wrong(message, whitelisted_channels, id, POKETWO_ID):

    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and f"<@{id}>" in message.content
        and "is the wrong pokémon" in message.content.lower()
    )

def not_enough_sahards(message, whitelisted_channels, id, POKETWO_ID):

    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and f"<@{id}>" in message.content
        and "You don't have enough shards" in message.content.lower()
    )

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


def convert_seconds(seconds):

    return humanfriendly.format_timespan(seconds)


def remove_diacritics(input_str):

    normalized_str = unicodedata.normalize("NFD", input_str)
    ascii_str = "".join(c for c in normalized_str if unicodedata.category(c) != "Mn")
    return ascii_str
