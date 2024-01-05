import discord
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
from dotenv import load_dotenv
from os import environ

import light_requests
from util import time_check, load_settings, check_for_config_files

load_dotenv()

if not check_for_config_files():
    raise RuntimeError(
        "Important config files are missing, please run setup.py first to generate them and then run main.py."
    )

SETTINGS = load_settings()
API_KEY = environ["API_KEY"]
MAC_ADDR = environ["DEVICE_MAC"]
MODEL_NUM = environ["DEVICE_MODEL_NUM"]
BOT_TOKEN = environ["BOT_TOKEN"]

intents = discord.Intents.default()
client = discord.Bot(intents=intents)


@client.event
async def on_application_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.respond(error)


@time_check(SETTINGS['start_time'], SETTINGS['end_time'])
@client.slash_command()
@cooldown(SETTINGS['cooldown_ceil'], SETTINGS['command_cooldown'], BucketType.guild)
async def setcolour(ctx, colour):
    request_body = light_requests.colour_change_body(
        MAC_ADDR, MODEL_NUM, colour=colour.lower()
    )

    if not request_body:
        await ctx.respond(f"{colour.title()} is not a valid colour.")
        await ctx.send(
            f"All colours:\n{', '.join(light_requests.all_colours()).title()}"
        )
        return

    success = light_requests.PUT(API_KEY, request_body)

    if success:
        await ctx.respond(f"Changing the light colour to {colour.title()}.")
    else:
        await ctx.respond(
            f"There was an error while changing the light colour to {colour.title()}."
        )


@time_check(SETTINGS['start_time'], SETTINGS['end_time'])
@client.slash_command()
@cooldown(SETTINGS['cooldown_ceil'], SETTINGS['command_cooldown'], BucketType.guild)
async def setrgb(ctx, r, g, b):
    if not r.strip().isdigit() or not g.strip().isdigit() or not b.strip().isdigit():
        await ctx.respond("Please enter numerical values.")
        return

    r, g, b = int(r), int(g), int(b)

    if not (0 <= r <= 255) or not (0 <= g <= 255) or not (0 <= b <= 255):
        await ctx.respond("Min: 0, Max: 255 for RGB values.")
        return

    request_body = light_requests.colour_change_body(MAC_ADDR, MODEL_NUM, rgb=(r, g, b))
    success = light_requests.PUT(API_KEY, request_body)

    if success:
        await ctx.respond(f"Changing the light colour to R: {r}, G: {g}, B: {b}.")
    else:
        await ctx.respond(
            f"There was an error while changing the light colour to R: {r}, G: {g}, B: {b}."
        )


@time_check(SETTINGS['start_time'], SETTINGS['end_time'])
@client.slash_command()
@cooldown(SETTINGS['cooldown_ceil'], SETTINGS['command_cooldown'], BucketType.guild)
async def setbrightness(ctx, brightness):
    if not brightness.strip().replace("%", "").isdigit():
        await ctx.respond("The brightness value must be a number.")
        return

    brightness = int(brightness.strip().replace("%", ""))

    if brightness not in range(1, 101):
        await ctx.respond("The brightness value must be between 1-100.")
        return

    request_body = light_requests.brightness_change_body(
        MAC_ADDR, MODEL_NUM, brightness
    )
    success = light_requests.PUT(API_KEY, request_body)

    if success:
        await ctx.respond(f"Changing the light brightness to {brightness}%")
    else:
        await ctx.respond(f"There was an error while changing the light brightness.")


@client.slash_command()
async def allcolours(ctx):
    await ctx.respond(
        f"All colours:\n{', '.join(light_requests.all_colours()).title()}"
    )


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


client.run(BOT_TOKEN)
