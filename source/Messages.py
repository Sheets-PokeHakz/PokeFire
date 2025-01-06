def is_shard_buy_message(message, whitelisted_channels, POKETWO_ID):
    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and "Are you sure you want to exchange".lower() in message.content.lower()
    )


def not_enough_sahards(message, whitelisted_channels, id, POKETWO_ID):
    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelisted_channels
        and f"<@{id}>" in message.content
        and "You don't have enough shards" in message.content.lower()
    )


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


def is_trade_accept(message, whitelist_channels, POKETWO_ID):
    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelist_channels
        and "Requesting a trade with" in message.content.lower()
    )


def is_trade_confirmation(message, whitelist_channels, POKETWO_ID):
    return (
        message.author.id == POKETWO_ID
        and message.channel.id in whitelist_channels
        and "Are you sure you want to confirm this trade?" in message.content.lower()
    )
