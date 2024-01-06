from configparser import ConfigParser
from os import path
from pathlib import Path
from datetime import datetime
from discord.ext import commands
import server


def can_alter_lights(start_time, end_time, commands_allowed):
    async def predicate(ctx):

        if not commands_allowed():
            await ctx.respond(
                "The host has currently disabled the ability to change or alter the lights. Please try again later when this functionality is enabled."
            )
            return False

        if start_time == end_time:
            return True

        current_hour = datetime.now().hour

        if start_time <= current_hour <= end_time:
            return True

        else:
            await ctx.respond(
                f"Business hours are from {start_time}:00 to {end_time}:00, please try again later."
            )
            return False

    start_time, end_time = int(start_time), int(end_time)
    return commands.check(predicate)


def load_settings() -> dict:
    config = ConfigParser()
    config.read(Path("./config.ini"))

    return {setting: value for setting, value in config["Settings"].items()}


def check_for_config_files() -> bool:
    existing_paths = [path.exists(Path('./.env')), path.exists(Path('./config.ini'))]
    return all(existing_paths)


def check_and_launch_server(using_server: bool, server_port: str) -> None:
    if not using_server:
        return None
    else:
        server.keep_alive(server_port)
