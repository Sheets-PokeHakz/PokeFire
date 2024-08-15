# System Modules
import time
import string
import random
import discord
import asyncio
import concurrent.futures

# Discord Modules
from discord.ext import commands, tasks
from discord_webhook import DiscordEmbed

# Pokefire Modules
from Source.CatptchaSolver import verify
from Source.PKIdentify import Pokefier
from Source.Utilities import *

# Initialize Pokefier Instance
pokefier = Pokefier()

# ========================================== CONFIG ========================================== #

config = read_config()

TOKENS = config["TOKENS"]

LOGGING = config["LOGGING"]
OWNER_ID = config["OWNER_ID"]
LANGUAGES = config["LANGUAGES"]
POKETWO_ID = config["POKETWO_ID"]

SPAM = config["SPAM"]["ENABLED"]
INTERVAL = config["SPAM"]["TIMING"]
SPAM_ID = config["SPAM"]["SPAM_ID"]
WEBHOOK_URL = config["WEBHOOK_URL"]

BLACKLISTED_POKEMONS = config["BLACKLISTED_POKEMONS"]
WHITELISTED_CHANNELS = config["WHITELISTED_CHANNELS"]

# ========================================== HINT ========================================== #

with open("Source/Pokemon", "r", encoding="utf8") as file:
    pokemon_list = file.read()


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])
    hint_string = "".join(hint)
    hint_replaced = hint_string.replace("_", ".")
    return re.findall("^" + hint_replaced + "$", pokemon_list, re.MULTILINE)


# ========================================== SPAM ========================================== #


def spam():

    with open("Messages/Messages.txt", "r", encoding="utf-8", errors="ignore") as file:
        messages = file.readlines()

    spam_message = random.choice(messages).strip()

    return spam_message


# ========================================== AUTOCATCHER CLASS ========================================== #


class Autocatcher(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, self_bot=False)

        self.spam_id = SPAM_ID
        self.interval = INTERVAL
        self.languages = LANGUAGES
        self.pokemon_data = load_pokemon_data()

        self.whitelisted_channels = WHITELISTED_CHANNELS
        self.blacklisted_pokemons = BLACKLISTED_POKEMONS

    async def solve_captcha(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return await asyncio.to_thread(verify, self)

    async def get_alternate_pokemon_name(self, name, languages=LANGUAGES):
        pokemon = next(
            (p for p in self.pokemon_data if p["name"].lower() == name.lower()), None
        )

        if pokemon:
            alternate_names = [
                alt_name
                for alt_name in pokemon.get("altnames", [])
                if alt_name.get("language").lower() in languages
            ]

            if alternate_names:
                return random.choice(alternate_names)["name"].lower()

        return name.lower()


# ========================================== MAIN FUNCTIONS ========================================== #


async def run_autocatcher(token):

    bot = Autocatcher()  # Initialize Bot

    @bot.event
    async def on_ready():

        print("+ ============== Pokefier ============== +")
        print(f"+ Logged In : {bot.user} (ID: {bot.user.id})")
        print("+ ============== Config ================ +")
        print(f"+ Languages: {bot.languages}")
        print(f"+ Whitelisted Channels: {bot.whitelisted_channels}")
        print(f"+ Blacklisted Pokemons: {bot.blacklisted_pokemons}")
        print("+ ====================================== +")

        bot.started = time.time()  # Stats The Time
        bot.command_prefix = f"<@{bot.user.id}> "  # Set Command Prefix

        print(f"+ Bot Prefix: {bot.command_prefix}")

        bot.verified = True  # Set Verified ( If False Bot Will Not Catch Pokemon)
        bot.pokemons_caught = 0  # Set Global Pokemon Counter To 0

        await spam_loop.start()

    # ========================================== SPAM TASKS ========================================== #

    enabled = SPAM
    interval = INTERVAL

    @tasks.loop(seconds=random.choice(interval))
    async def spam_loop():

        if bot.verified and enabled == "True" and SPAM_ID:
            channel = bot.get_channel(SPAM_ID)
            await channel.send(spam())

    @bot.command()
    async def start(ctx):

        if ctx.author.id == OWNER_ID:
            await spam_loop.start()

            embed = DiscordEmbed(title="Spamming Started", color="046e1f")
            embed.set_author(
                name="Pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )

            await send_log(embed=embed)

            data = read_config()
            data["SPAM"]["ENABLED"] = "True"

            with open("Source/Config.json", "w") as file:
                json.dump(data, file, indent=4)

            await ctx.send("I am working hard dude")

        else:

            embed = DiscordEmbed(
                title="Nah Sorry Bro",
                description="Only Owners Can Use It",
                color="046e1f",
            )
            embed.set_author(
                name="Pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )

            await send_log(embed=embed)
            await ctx.send("# You Are Not My Owner")

    @bot.command()
    async def stop(ctx):

        if ctx.author.id == OWNER_ID:
            await spam_loop.stop()

            embed = DiscordEmbed(title="Spamming Stopped", color="046e1f")
            embed.set_author(
                name="Pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )

            await send_log(embed=embed)

            data = read_config()
            data["SPAM"]["ENABLED"] = "False"

            with open("Source/Config.json", "w") as file:
                json.dump(data, file, indent=4)

            await ctx.send("I am taking a break dude")

        else:
            embed = DiscordEmbed(
                title="Nah Sorry Bro",
                description="Only Owners Can Use It",
                color="046e1f",
            )
            embed.set_author(
                name="Pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )

            await send_log(embed=embed)
            await ctx.send("# You Are Not My Owner")

    @bot.command()
    async def ping(ctx):

        await ctx.send("Pong!")
        await ctx.send(f"Latency : {round(bot.latency * 1000)}ms")

    @bot.command()
    async def incense(ctx, time: str, inter: str):

        if ctx.author.id != OWNER_ID:
            if time in ["30m", "1h", "3h", "1d"] and inter in ["10s", "20s", "30s"]:
                await ctx.send(f"<@{POKETWO_ID}> incense buy {time} {inter} -y")

        else:
            await ctx.send(
                f"Invalid Usage. Correct Usage : `{bot.command_prefix}incense <time> <interval>`"
            )
            await ctx.send("Time : 30m, 1h, 3h, 1d")
            await ctx.send("Interval : 10s, 20s, 30s")

    @bot.command()
    async def shardbuy(ctx, amt: int):

        if ctx.author.id == OWNER_ID:
            if amt > 0:
                await ctx.send(f"<@{POKETWO_ID}> buy shards {amt}")
        else:
            await ctx.send(
                f"Invalid Usage. Correct Usage : `{bot.command_prefix}shardbuy <amount>`"
            )

    @bot.command()
    async def channeladd(ctx, *channel_ids):

        if not channel_ids:
            await ctx.reply(
                "`You Must Provide Atleast One Channel ID. Separate Multiple IDs With Spaces.`"
            )
            return

        message = "```\n"

        for channel_id_str in channel_ids:
            try:
                channel_id = int(channel_id_str)
            except ValueError:
                await ctx.reply(
                    f"Invalid Channel ID : `{channel_id_str}`. Please Provide A Valid Numeric Channel ID."
                )
                continue

            if channel_id in bot.whitelisted_channels:
                message += f"Channel ID : {channel_id} Is Already Whitelisted\n"
            else:
                bot.whitelisted_channels.append(channel_id)
                message += f"Channel ID : {channel_id} Whitelisted\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def channelremove(ctx, *channel_ids):

        if not channel_ids:
            await ctx.reply(
                "`You Must Provide Atleast One Channel ID. Separate Multiple IDs With Spaces.`"
            )
            return

        message = "```\n"

        for channel_id_str in channel_ids:
            try:
                channel_id = int(channel_id_str)
            except ValueError:
                await ctx.reply(
                    f"Invalid Channel ID : `{channel_id_str}`. Please Provide A Valid Numeric Channel ID."
                )
                continue

            if channel_id in bot.whitelisted_channels:
                bot.whitelisted_channels = [
                    ch_id for ch_id in bot.whitelisted_channels if ch_id != channel_id
                ]
                message += f"Channel ID : {channel_id} Removed From Whitelist\n"
            else:
                message += f"Channel ID : {channel_id} Is Not Whitelisted\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def languageadd(ctx, *languages):

        if not languages:
            await ctx.reply(
                "`You Must Provide Atleast One Language. Separate Multiple Languages With Spaces.`"
            )
            return

        message = "```\n"
        valid_languages = ["english", "french", "german", "japanese"]

        for language in languages:
            if language.lower() not in valid_languages:
                await ctx.reply(
                    f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                )
                continue

            if language.lower() in bot.languages:
                message += f"Language : {language} Is Already Added\n"
            else:
                bot.languages.append(language.lower())
                message += f"Language : {language} Added\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def languageremove(ctx, *languages):

        if not languages:
            await ctx.reply(
                "`You Must Provide Atleast One Language. Separate Multiple Languages With Spaces.`"
            )
            return

        message = "```\n"
        valid_languages = ["english", "french", "german", "japanese"]

        for language in languages:
            if language.lower() not in valid_languages:
                await ctx.reply(
                    f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                )
                continue

            if language.lower() in bot.languages:
                bot.languages = [lang for lang in bot.languages if lang != language]
                message += f"Language : {language} Removed\n"
            else:
                message += f"Language : {language} Is Not Added\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def blacklistadd(ctx, *pokemons):

        if not pokemons:
            await ctx.reply(
                "`You Must Provide Atleast One Pokemon. Separate Multiple Pokemons With Spaces.`"
            )
            return

        message = "```\n"
        bot.blacklisted_pokemons = [
            pokemon_name.lower() for pokemon_name in bot.blacklisted_pokemons
        ]

        for pokemon in pokemons:
            if pokemon.lower() in bot.blacklisted_pokemons:
                message += f"Pokemon: {pokemon} Is Already Blacklisted\n"
            else:
                bot.blacklisted_pokemons.append(pokemon.lower())
                message += f"Pokemon: {pokemon} Added To Blacklist\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def blacklistremove(ctx, *pokemons):

        if not pokemons:
            await ctx.reply(
                "`You Must Provide Atleast One Pokemon. Separate Multiple Pokemons With Spaces.`"
            )
            return

        message = "```\n"
        bot.blacklisted_pokemons = [
            pokemon_name.lower() for pokemon_name in bot.blacklisted_pokemons
        ]

        for pokemon in pokemons:
            if pokemon.lower() in bot.blacklisted_pokemons:
                bot.blacklisted_pokemons = [
                    poke for poke in bot.blacklisted_pokemons if poke != pokemon
                ]
                message += f"Pokemon : {pokemon} Removed From Blacklist\n"
            else:
                message += f"Pokemon : {pokemon} Is Not Blacklisted\n"

        message += "```"
        await ctx.send(message)

    @bot.command()
    async def config(ctx):

        message = f"```PREFIX: {bot.command_prefix}\nOWNER_ID: {OWNER_ID}\n\nWHITELISTED_CHANNELS = {bot.whitelisted_channels}\nBLACKLISTED_POKEMONS={bot.blacklisted_pokemons}\n\nLANGUAGES = {bot.languages}```"
        await ctx.reply(message)

    @bot.command()
    async def say(ctx, *, message):

        if ctx.message.author.id != OWNER_ID:
            return
        else:
            await ctx.send(message)

    @bot.event
    async def on_message(message):

        await bot.process_commands(message)

        if (
            is_shard_buy_message(message, bot.whitelisted_channels, POKETWO_ID)
            and bot.verified
        ):

            print("[?] A Shard Buy Message Received")

            await message.components[0].children[0].click()


        if (
            is_spawn_message(message, bot.whitelisted_channels, POKETWO_ID)
            and bot.verified
        ):
            
            print("[?] A Pokémon Spawned")

            await spam_loop.stop()

            pokemon_image = message.embeds[0].image.url
            predicted_pokemons = await pokefier.predict_pokemon_from_url(pokemon_image)

            predicted_pokemon = max(predicted_pokemons, key=lambda x: x[1])

            name = predicted_pokemon[0]
            score = predicted_pokemon[1]

            bot.blacklisted_pokemons = [
                pokemon_name.lower() for pokemon_name in bot.blacklisted_pokemons
            ]

            if name.lower() in bot.blacklisted_pokemons:
                print(f"[?] Pokémon : {name} Was Not Caught Because It Is Blacklisted")
                return

            if score > 30.0:
                alt_name = await bot.get_alternate_pokemon_name(
                    name, languages=bot.languages
                )
                alt_name = remove_diacritics(alt_name)

                await message.channel.send(f"<@716390085896962058> c {alt_name}")

        if (
            is_captcha_message(
                message, bot.whitelisted_channels, bot.user.id, POKETWO_ID
            )
            and bot.verified
        ):
            print("[?] A Captcha Challenge Was Received")

            await spam_loop.stop()

            bot.verified = False
            started = time.time()
            await bot.solve_captcha()

            if LOGGING == 1:
                elapsed = convert_seconds(round((time.time() - started)))
                uptime = convert_seconds(round(time.time() - bot.started))

                embed = DiscordEmbed(title="A Captcha Was Solved!", color="046e1f")
                embed.set_description(
                    f"Account Name : {bot.user.name}\n\nTime Taken : {elapsed}\nAccount Uptime : {uptime}"
                )
                embed.set_author(
                    name="Pokefier",
                    url="https://github.com/sayaarcodes/pokefier",
                    icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
                )

                send_log(embed, WEBHOOK_URL)

        if (
            not_enough_sahards(
                message, bot.whitelisted_channels, bot.user.id, POKETWO_ID
            )
            and bot.verified
        ):

            await spam_loop.stop()

            print("[?] Not Enough Shards To Buy Incense")

            await message.channel.send(f"Not Enough Shards To Buy Incense")
            await message.channel.send(f"To Buy Shards Use `{bot.command_prefix}shardbuy <amount>`")

        if (
            is_pokemon_wrong(message, bot.whitelisted_channels, bot.user.id, POKETWO_ID)
            and bot.verified
        ):

            await spam_loop.stop()

            hint = solve(message.content)

            if hint:
                await message.channel.send(f"<@{POKETWO_ID}> c {hint[0]}")

        if (
            is_pokemon_caught_message(
                message, bot.whitelisted_channels, bot.user.id, POKETWO_ID
            )
            and LOGGING == 1
        ):
            bot.pokemons_caught += 1

            if SPAM == "True":
                await spam_loop.start()

            is_shiny = False
            if "these colors" in message.content.lower():
                is_shiny = True

            pokemon_data = extract_pokemon_data(message.content)
            pokemon = next(
                (
                    p
                    for p in bot.pokemon_data
                    if p["name"].lower() == pokemon_data["name"].lower()
                ),
                None,
            )

            embed = DiscordEmbed(title="A Pokemon Was Caught!", color="03b2f8")
            embed.set_description(
                f"Account Name : {bot.user.name}\n\nPokémon Name : {pokemon_data['name']}\n\nPokémon Level : {pokemon_data['level']}\nPokémon IV : {pokemon_data['IV']}%\n\nShiny : {is_shiny}\nRarity : {pokemon['rarity']}\n\nPokémons Caught : {bot.pokemons_caught}"
            )
            embed.set_author(
                name="Pokefier",
                url="https://github.com/sayaarcodes/pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )
            embed.set_thumbnail(url=pokemon["image"]["url"])
            embed.set_timestamp()

            send_log(embed, WEBHOOK_URL)

    await bot.start(token)


async def main(tokens):

    tasks = [run_autocatcher(token) for token in tokens]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main(TOKENS))
