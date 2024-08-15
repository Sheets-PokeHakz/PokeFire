# Documentation

This document provides detailed information about the functions used in the project.

-----

## Table of Contents [ Main.py ]

- [solve_captcha](#solve_captcha)
- [get_alternate_pokemon_name](#get_alternate_pokemon_name)
- [run_autocatcher](#run_autocatcher)
- [on_ready](#on_ready)
- [spam_loop](#spam_loop)
- [start](#start)
- [stop](#stop)
- [ping](#ping)
- [incense](#incense)
- [config](#config)
- [channeladd](#channeladd)
- [channelremove](#channelremove)
- [blacklistadd](#blacklistadd)
- [blacklistremove](#blacklistremove)
- [on_message](#on_message)

## solve_captcha()

**Description:**
Solves the captcha challenge asynchronously by calling the verify function. Returns `True` if the captcha is solved properly.

**Arguments:**

- None

**Returns:**

- `bool`: `True` if the captcha is solved properly, `False` otherwise.

## get_alternate_pokemon_name()

**Description:**
Retrieves an alternate name for a Pokémon in the specified languages.

**Arguments:**

1. `name` (str): The Pokémon name to find alternates for.
2. `languages` (list of str): The list of languages to consider.

**Returns:**

- `str`: The alternate Pokémon name, or the original name if no alternate is found.

## run_autocatcher()

**Description:**
Runs the autocatcher bot.

**Arguments:**

1. `token` (str): The token to authenticate the bot.

**Returns:**

- `None`

## on_ready()

**Description:**
Event processed while starting the bot, displays important settings.

## spam_loop()

**Description:**
Main function to loop the spam checking in all the required varibles to start spamming.

**Arguments:**

1. `intervals` (list): The time after which each message would be sent.

**Returns:**

- `str` : Sends the message in the particular spam channel.

## start()

**Description:**
Command to start spamming.

**Arguments:**

- `None` 

**Returns:**

1. `ctx (discord.ext.commands.Context)` : The command context. 

## stop()

**Description:**
Command to stop spamming.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context. 

**Returns:**

- `None`

## ping()

**Description:**
Responds with 'Pong!' to check if the bot is responsive.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context. 

**Returns:**

- `None`

## incense()

**Description:**
Buy an incense for the bot.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `time (string)` : Amount of time the incese will run. [ Time : 30m, 1h, 3h, 1d ]
3. `inter (string)` : Amount of time between each spawn in incense. [ Interval : 10s, 20s, 30s ]  

**Returns:**

- `None`

## shardbuy()

**Description:**
Buy shards to run the incense.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `amt (int)` : Amout of shards to buy. 

**Returns:**

- `None`

## channeladd()

**Description:**
Adds a channel ID to the whitelist.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `channel_ids (str)` : A list of channel IDs separated by spaces.

**Returns:**

- `None`

## channelremove()

**Description:**
Removes a channel ID to the whitelist.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `channel_ids (str)` : A list of channel IDs separated by spaces.

**Returns:**

- `None`

## languageadd()

**Description:**
Adds a language to use while catching Pokemon.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `languages (str)` : A list of languages separated by spaces.

**Returns:**

- `None`

## languageremove()

**Description:**
Removes a language to use while catching Pokemon.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `languages (str)` : A list of languages separated by spaces.

**Returns:**

- `None`

## blacklistadd()

**Description:**
Adds a pokemon to blacklist.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `pokemons (str)` : A list of pokemons separated by spaces.

**Returns:**

- `None`

## blacklistremove()

**Description:**
Removes a pokemon from blacklist.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `pokemons (str)` : A list of pokemons separated by spaces.

**Returns:**

- `None`

## config()

**Description:**
Displays the current bot configuration.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.

**Returns:**

- `None`

## say()

**Description:**
Sends a message if the author is the owner.

**Arguments:**

1. `ctx (discord.ext.commands.Context)` : The command context.
2. `message (str)` : The message to send.

**Returns:**

- `None`

## on_message()

**Description:**
Event handler for when a message is received.

**Arguments:**

1. `message (discord.Message)` : The received message.

**Returns:**

- `None`

-------

## Table Of Contents [ Utilities.py ]

- [read_config](#read_config)
- [send_log](#send_log)
- [is_spawn_message](#is_spawn_message)
- [is_captcha_message](#is_captcha_message)
- [is_pokemon_caught_message](#is_pokemon_caught_message)
- [extract_pokemon_data](#extract_pokemon_data)
- [load_pokemon_data](#load_pokemon_data)
- [convert_seconds](#convert_seconds)

## read_config()

**Description:**
Reads a JSON configuration file and returns its contents as a dictionary.

**Arguments:**

1. `filename (str)` : The path to the configuration file. Default is 'SRC/Config.json'.

**Returns:**

1. `dict` : The contents of the configuration file as a dictionary.

## send_log()

**Description:**
Sends a log message to a specified Discord webhook URL.

**Arguments:**

1. `embed (DiscordEmbed)` : An embed object that contains the message to be sent to the Discord webhook.
2. `WEBHOOK_URL (str)` : The URL of the Discord webhook where the log message will be sent.

**Returns:**

- `None`

## is_spawn_message()

**Description:**
Checks if the message is a spawn message from Poketwo in a whitelisted channel.

**Arguments:**

1. `message (discord.Message)` : The message to check.
2. `whitelisted_channels (list)` : The list of whitelisted channel IDs.

**Returns:**

1. `bool` : True if the message is a spawn message, False otherwise.

## is_captcha_message()

**Description:**
Checks if the message contains a captcha challenge from Poketwo in a whitelisted channel.

**Arguments:**

1. `message (discord.Message)` : The message to check.
2. `whitelisted_channels (list)` : The list of whitelisted channel IDs.
3. `id (int)` : The user ID to verify against.

**Returns:**

1. `bool` : True if the message is a captcha challenge, False otherwise.

## is_pokemon_caught_message()

**Description:**
Checks if a message indicates that a Pokémon was caught.

**Arguments:**

1. `message (discord.Message)` : The message to check.
2. `whitelisted_channels (list)` : The list of whitelisted channel IDs.
3. `id (int)` : The ID of the account.

**Returns:**

1. `bool` : True if the message meets the criteria for a Pokémon caught message, False otherwise.

## extract_pokemon_data()

**Description:**
Extracts Pokemon data from a given text.

**Arguments:**

1. `text (str)` : The text containing information about the captured Pokemon.

**Returns:**

1. `dict` or `None` : A dictionary containing the extracted Pokemon data, including level, name, and IV (Individual Value), or None if no match is found.

## load_pokemon_data()

**Description:**
Loads Pokémon data from a JSON file.

**Arguments:**

- `None`

**Returns:**

1. `dict` : The loaded Pokémon data.

## convert_seconds()

**Description:**
Converts a given number of seconds into a human-friendly timespan string.

**Arguments:**

1. `seconds (int)` : The number of seconds to convert.

**Returns:**

1. `str` : The human-friendly timespan string.

## remove_diacritics()

**Description:**
Removes diacritics from a given string, converting characters to their base forms.

**Arguments:**

1. `input_str (str)` : The input string potentially containing diacritics.

**Returns:**

1. `str` : The string with diacritics removed.

-------

## Table Of Contents [ CaptchaSolver.py ]

- [download_audio]()
- [convert_mp3_to_wav]()
- [recognize_audio]()
- [solve_captcha]()
- [verify]()

## download_audio()

**Description:**
Downloads the captcha audio file from the specified URL and saves it to the given file path.

**Arguments:**

1. `driver` : The selenium driver instance.
2. `download_button` : The CSS selector for the download button.
3. `file_path` : The path where the audio file will be saved.

**Returns:**

- `None`

## convert_mp3_to_wav()

**Description:**
Converts an MP3 file to WAV format.

**Arguments:**

1. `mp3_path` : The path to the MP3 file.
2. `wav_path` : The path where the converted WAV file will be saved.

**Returns:**

- `None`

## recognize_audio()

**Description:**
Recognizes text from the given WAV audio file using Google's speech recognition API.

**Arguments:**

1. `wav_path` : The path to the WAV audio file.

**Returns:**

1. Recognized text as a string.

## solve_captcha()

**Description:**
Recognizes text from the given WAV audio file using Google's speech recognition API.

**Arguments:**

1. `driver` : The selenium driver instance.
2. `id` : The user's ID.

**Returns:**

1. True if captcha was solved successfully, False otherwise.

## verify()

**Description:**
Continuously attempts to verify the bot until successful.

**Arguments:**

1. `bot` : The bot instance to be verified.

**Returns:**

- `None`

