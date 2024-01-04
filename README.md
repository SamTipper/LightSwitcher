# LightSwitcher
*A discord bot that changes the colour of your Govee light.*

## Setup:
### DISCLAIMER: PLEASE DO NOT SHARE YOUR GOVEE API KEY, DISCORD BOT TOKEN, OR YOUR .ENV FILE WITH ANYONE. I AM NOT RESPONSIBLE FOR ANYTHING THAT HAPPENS AFTER BREACHING THIS DISCLAIMER.
**Make sure you have your Govee API key and you have created a discord bot. Keep both your API key and Discord bot token handy.**

1. Clone the repository, create a virtual environment, and activate it.
   - Windows `python -m venv ./` | `source activate`
   - Linux/OSX `python -m venv ./` | `source ./bin/activate`

2. Install the requirements. `pip install -r requirements.txt`
3. Run the `setup.py` script, you will need to enter your Govee API key and Discord bot token immediately, so get them both ready.
4. Once the setup script is complete and has created your .env and config files, you can run `main.py` script and your bot should be ready to go!
5. Start inviting your bot to Discord channels, make sure it has all intents enabled, and give it these OAuth2 permissions:
   
    **Scopes:**
    - bot
    - applications.commands

    **Bot Permissions:**
    - Send Messages
    - Send Messages in Threads
    - Read Message History
    - Use Slash Commands

If you spot any bugs or anything that seems wrong, please feel free to raise an issue.

## Commands:
1. `/setcolour [colour]`
2. `/setrgb [r], [g], [b]`
3. `/setbrightness [1-100]`

I plan to add more commands in the future, feel free to contribute to this project to bulk out its functionality!

## Config:
Once you run the setup, the `config.ini` file will be made. You don't need to touch this file but you can if you aren't happy with a few of the program's behaviours.

### All Configurable Settings:
- **start_time** (INTEGER): The initial time of day when the program will accept commands. It accepts integers that are 1 or 2 characters in length, representing the hour in a day.

- **end_time** (INTEGER): The final time of day when the program will accept commands. It accepts integers that are 1 or 2 characters in length, representing the hour in a day.

- **cooldown_ceil** (INTEGER): The maximum number of times commands can be used before the cooldown is triggered (global).

- **command_cooldown** (INTEGER): The duration of a command cooldown in seconds (global).

## Limitations:
The Govee API has a few limitations:
1. 10,000 API requests per day.
2. 10 API requests per minute.

I have added individual 60-second cooldowns for each command, this ensures that you shouldn't get anywhere near the rate limit within a minute or day. This of course can be changed in the `config.ini` file, but I highly recommend that you don't.
