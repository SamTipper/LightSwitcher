# LightSwitcher
*A discord bot that changes the colour of your Govee light.*

## Setup:
### DISCLAIMER: PLEASE DO NOT SHARE YOUR GOVEE API KEY, DISCORD BOT TOKEN, .ENV FILE, OR YOUR CONFIG FILE WITH ANYONE. I AM NOT RESPONSIBLE FOR ANYTHING THAT HAPPENS AFTER BREACHING THIS DISCLAIMER.
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
4. `/allcolours`

I plan to add more commands in the future, feel free to contribute to this project to bulk out its functionality!

## Config:
Once you run the setup, the `config.ini` file will be made. You don't need to touch this file but you can if you aren't happy with a few of the program's behaviours.

### All Configurable Settings:
- **start_time** (INTEGER): The initial time of day when the program will accept commands. It accepts integers that are 1 or 2 characters in length, representing the hour of day in 24h clock format.

- **end_time** (INTEGER): The final time of day when the program will accept commands. It accepts integers that are 1 or 2 characters in length, representing the hour of day in 24h clock format.

- **cooldown_ceil** (INTEGER): The maximum number of times commands can be used before the cooldown is triggered (global).

- **command_cooldown** (INTEGER): The duration of a command cooldown in seconds (global).

- **use_server** (BOOLEAN): Tells the script whether to run a small Flask web-server that allows you to pause and un-pause light alteration requests. Read more about this in the "Server" section.

- **server_port** (INTEGER): Configures the port the server will use if the `use_server` setting is `true`.

- **api_key** (STRING): If set to 0, the server will not use an API key. If set to any other number, the server will require the `Authorization: api_key` header.

## Server:
By default, the config file has `use_server` set to `false`. When you set this to setting to `true`, the script will launch a Flask-based API on a seperate thread that will listen for HTTP requests.

There is currently one endpoint that you can use that does anything at the moment `http://server.ip:port/toggle` allows you to toggle all incoming light change commands on and off. It's as simple as just sending a get request to the endpoint and it handles the rest! It will send you a response body that tells you if the setting is toggled on or off. You will receive an automatically generated API key in the config file, this can be changed if you are not happy with it. Alternatively, you can change it to `0` to tell the server that you don't want to use an API key, ommiting the `Authorization` header.

## Limitations:
The Govee API has a few limitations:
1. 10,000 API requests per day.
2. 10 API requests per minute.

I have added individual 60-second cooldowns for each command, this ensures that you shouldn't get anywhere near the rate limit within a minute or day. This of course can be changed in the `config.ini` file, but I highly recommend that you don't.
