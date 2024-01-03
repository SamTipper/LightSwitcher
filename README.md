# LightSwitcher
*A discord bot that changes the colour of your Govee light.*

## Setup
### DISCLAIMER: PLEASE DO NOT SHARE YOUR GOVEE API KEY, DISCORD BOT TOKEN, OR YOUR .ENV FILE WITH ANYONE. I AM NOT RESPONSIBLE FOR ANYTHING THAT HAPPENS PRIOR TO BREACHING THIS DISCLAIMER.
**Make sure you have your Govee API key and have created a discord bot. Keep both your API key and Discord bot token handy.**

1. Clone the respository and install the requirements. `pip install -r requirements.txt`
2. Run the `setup.py` script, you will need to enter your Govee API key and Discord bot token so get them both ready.
3. Once the setup file is complete and has created your .env file, you can run `main.py` script and your bot should be ready to go!
4. Start inviting your bot to Discord channels, make sure it has all intents enabled and give it these OAuth2 permissions:
    **Scopes:**
    - bot
    - applications.commands

    **Bot Permissions:**
    - Send Messages
    - Send Messages in Threads
    - Read Message History
    - Use Slash Commands

If you spot any bugs or anything that doesn't seem right, please feel free to raise an issue.