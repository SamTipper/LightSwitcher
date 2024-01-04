import configparser
from pathlib import Path
from datetime import datetime
from discord.ext import commands


def time_check(business_hours_start, business_hours_end):
    async def predicate(ctx):
        current_hour = datetime.now().hour

        if business_hours_start <= current_hour <= business_hours_end:
            return True

        else:
            await ctx.respond(
                f"Business hours are from {business_hours_start}:00 to {business_hours_end}:00, please try again later."
            )
            return False

    return commands.check(predicate)


def load_settings() -> dict:
    config = configparser.ConfigParser()
    config.read(Path('./config.ini'))

    return {setting: value for setting, value in config['Settings'].items()}
