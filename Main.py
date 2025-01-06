# System Modules
import time
import json
import random
import asyncio
import logging

# Discord Modules
from discord.ext import commands
from discord_webhook import DiscordEmbed

# Pokefire Modules
from source.PKIdentify import Pokefier
from source.Utilities import (
    extract_pokemon_data,
    load_pokemon_data,
    remove_diacritics,
    read_config,
    send_log,
    solve,
)

# Initialize Pokefier Instance
pokefier = Pokefier()

# ========================================== LOGGING ========================================= #

# Defining The Basic logger.info Message For logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Defining The Logger
logger = logging.getLogger(__name__)


# Defining The Log Message Function
def log_message(level, message):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.info(message)


logger.info("Initialized Logging")

# ========================================== CONFIG ========================================== #

# Reading The Config File
config = read_config()
logger.info("Initialized Config")

# Defining The Config Variables
DELAY = config["DELAY"]
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
        logger.info("+ ============== Pokefier ============== +")
        logger.info(f"+ Logged In : {bot.user} (ID: {bot.user.id})")
        logger.info("+ ============== Config ================ +")
        logger.info(f"+ Languages: {bot.languages}")
        logger.info(f"+ Whitelisted Channels: {bot.whitelisted_channels}")
        logger.info(f"+ Blacklisted Pokemons: {bot.blacklisted_pokemons}")
        logger.info("+ ====================================== +")

        bot.started = time.time()  # Stats The Time
        bot.command_prefix = f"<@{bot.user.id}> "  # Set Command Prefix

        logger.info(f"+ Bot Prefix: {bot.command_prefix}")

        bot.verified = True  # Set Verified ( If False Bot Will Not Catch Pokemon)
        bot.pokemons_caught = 0  # Set Global Pokemon Counter To 0

    # ========================================== SPAM TASKS ========================================== #

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

        # ========================================== TRADE HANDLING ========================================== #

        if (
            message.author.id == POKETWO_ID
            and message.channel.id in bot.whitelisted_channels
        ):
            # Stop Spamming

            logger.info("Message Received From POKETWO")
            logger.info("Attempting To Process Message")

            # Trade Accept
            if "requesting a trade with" in message.content.lower():
                logger.info("Trade Request Received")

                if (
                    message.components[0].children[0].label.lower() == "accept"
                ):  # Checking If Accept Button Is Present
                    await time.sleep(
                        random.choice(DELAY)
                    )  # Delay Before Accepting Trade For Human Replication
                    await (
                        message.components[0].children[0].click()
                    )  # Clicking The Accept Button

                logger.info("Trade Accepted")
                # Start Spamming

            # Trade Confirmation
            if message.embeds:
                if (
                    "are you sure you want to confirm this trade? please make sure that you are trading what you intended to."
                    in message.embeds[0].description.lower()
                ):
                    logger.info("Trade Confirmation Received")

                    if (
                        message.components[0].children[0].label.lower() == "confirm"
                    ):  # Checking If Confirm Button Is Present
                        await time.sleep(
                            random.choice(DELAY)
                        )  # Delay Before Confirming Trade For Human Replication
                        await (
                            message.components[0].children[0].click()
                        )  # Clicking The Confirm Button

                    logger.info("Trade Completed")
                    # Start Spamming

        # ========================================== SHARDS HANDLING ========================================== #

        if "are you sure you want to exchange" in message.content.lower():
            # Stop Spamming

            logger.info("A Shard Buy Message Received")

            if (
                message.components[0].children[0].label.lower() == "confirm"
            ):  # Checking If Confirm Button Is Present
                await time.sleep(
                    random.choice(DELAY)
                )  # Delay Before Confirming Trade For Human Replication
                await (
                    message.components[0].children[0].click()
                )  # Clicking The Confirm Button

            logger.info("Shard Bought")
            # Start Spamming

        if "you don't have enough shards" in message.content.lower():
            # Stop Spamming

            logger.info("Not Enough Shards To Buy Incense")

            await message.channel.send("Not Enough Shards To Buy Incense")
            await message.channel.send(
                f"To Buy Shards Use `{bot.command_prefix}shardbuy <amount>`"
            )
            # Start Spamming

        # ========================================== SPAWN HANDLING ========================================== #

        incense = ""
        remaning_spawns = ""
        spawn_interval = ""
        time_left = ""

        if message.embeds:
            if (
                "wild" in message.embeds[0].title.lower() and bot.verified
            ):  # Checking If Pokémon Spawned And Bot Is Verified
                logger.info("A Pokémon Spawned - Attemping To Predict")

                # Stop Spamming

                if message.embeds[0].footer.text:
                    footer = message.embeds[0].footer.text

                    footer.split("\n")
                    incense = footer[0]
                    remaning_spawns = footer[1]
                    spawn_interval = footer[2]
                    time_left = footer[3].split("at")[0]

                pokemon_image = message.embeds[
                    0
                ].image.url  # Get The Image URL Of The Pokémon
                predicted_pokemons = await pokefier.predict_pokemon_from_url(
                    pokemon_image
                )  # Predict The Pokémon Using Pokefier

                predicted_pokemon = max(
                    predicted_pokemons, key=lambda x: x[1]
                )  # Get The Pokémon With Highest Score

                name = predicted_pokemon[0]  # Get The Name Of The Pokémon
                score = predicted_pokemon[1]  # Get The Score Of The Pokémon

                bot.blacklisted_pokemons = [
                    pokemon_name.lower() for pokemon_name in bot.blacklisted_pokemons
                ]  # Get The Blacklisted Pokemons

                if name.lower() in bot.blacklisted_pokemons:
                    logger.info(
                        f"Pokémon : {name} Was Not Caught Because It Is Blacklisted"
                    )
                    return

                if score > 30.0:  # 30 Is The Threshold Score
                    alt_name = await bot.get_alternate_pokemon_name(
                        name, languages=bot.languages
                    )
                    alt_name = remove_diacritics(alt_name)

                    await message.channel.send(f"<@716390085896962058> c {alt_name}")
                    logger.info(f"Predicted Pokémon : {name} With Score : {score}")

                else:
                    logger.info(f"Predicted Pokémon : {name} With Score : {score}")

        if "that is the wrong pokémon" in message.content.lower() and bot.verified:
            # Stop Spamming

            logger.info("Wrong Pokémon Detected")
            await message.channel.send("<@716390085896962058> h")

            logger.info("Requested Hint For Wrong Pokémon")

        if "the pokémon is" in message.content.lower() and bot.verified:
            logger.info("Solving The Hint")
            await message.channel.send(
                "<@716390085896962058> c {}".format(solve(message.content))
            )

            logger.info("Hint Solved")

        # ========================================== CATCH LOG HANDLING ========================================== #
        incense = False
        remaning_spawns = ""
        spawn_interval = ""
        time_left = ""

        if "congratulations" in message.content.lower() and bot.verified:
            bot.pokemons_caught += 1

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

            embed1 = DiscordEmbed(title="A Pokemon Was Caught!", color="03b2f8")
            embed1.set_description(
                f"Account Name : {bot.user.name}\n\nPokémon Name : {pokemon_data['name']}\n\nPokémon Level : {pokemon_data['level']}\nPokémon IV : {pokemon_data['IV']}%\n\nShiny : {is_shiny}\nRarity : {pokemon['rarity']}\n\nPokémons Caught : {bot.pokemons_caught}"
            )
            embed1.set_author(
                name="Pokefier",
                url="https://github.com/sayaarcodes/pokefier",
                icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
            )
            embed1.set_thumbnail(url=pokemon["image"]["url"])
            embed1.set_timestamp()

            if incense.lower() == "Incense: Active.".lower():
                embed2 = DiscordEmbed(title="Incense Details", color="03b2f8")
                embed2.set_description(
                    f"Remaining Spawns : {remaning_spawns}\nSpawn Interval : {spawn_interval}\nTime Left : {time_left}"
                )

                embed2.set_author(
                    name="Pokefier",
                    url="https://github.com/sayaarcodes/pokefier",
                    icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
                )

                embed2.set_thumbnail(url=pokemon["image"]["url"])
                embed2.set_timestamp()

                await send_log(embed=embed2, WEBHOOK_URL=WEBHOOK_URL)

            await send_log(embed=embed1, WEBHOOK_URL=WEBHOOK_URL)

        # ========================================== CAPTCHA HANDLING ========================================== #

        if (
            f"https://verify.poketwo.net/captcha/{bot.user.id}" in message.content
            and bot.verified
        ):
            logger.info("A Captcha Challenge Was Received")
            # Stop Spamming

            bot.verified = False
            await message.channel.send("<@716390085896962058> incense pause")
            logger.info("Incense Paused")

            owner_dm = await bot.fetch_user(OWNER_ID)
            await owner_dm.send(
                f"Captcha Challenge Received. Please Solve It.\n\n{message.content}"
            )
            logger.info("Captcha Challenge Sent To Owner")

    await bot.start(token)


async def main(tokens):
    ac_tasks = [run_autocatcher(token) for token in tokens]
    await asyncio.gather(*ac_tasks)


if __name__ == "__main__":
    asyncio.run(main(TOKENS))
