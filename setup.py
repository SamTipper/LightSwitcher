import requests
import textwrap
from pathlib import Path
from secrets import token_hex


def get_tokens() -> str:
    api_key = input("Please enter your Govee API key:\n").strip()
    bot_token = input("Please enter your Discord bot token:\n").strip()
    return api_key, bot_token


def get_devices(api_key: str) -> list | None:
    response = requests.get(
        "https://developer-api.govee.com/v1/devices", headers={"Govee-API-Key": api_key}
    )

    if response.status_code == 401:
        print(
            f"There was an error retriving your device information, here is the error: {response.json()['message']}"
        )
        return

    response = response.json()

    filtered_devices = [
        device for device in response["data"]["devices"] if "deviceName" in device
    ]
    return filtered_devices


def list_devices(filtered_devices: list) -> dict | None:
    print("Please type the number of device you would like to control:\n")

    for index, device in enumerate(filtered_devices):
        print(f"{index}: {device['deviceName']}")

    chosen_device = input()
    if not chosen_device.strip().isdigit():
        return

    chosen_device_index = int(chosen_device.strip())

    if chosen_device_index not in range(0, len(filtered_devices)):
        return

    return filtered_devices[chosen_device_index]


def create_env_file(api_key: str, bot_token: str, chosen_device: dict) -> None:
    env_data = f"API_KEY = {api_key}\nDEVICE_MAC = {chosen_device['device']}\nDEVICE_MODEL_NUM = {chosen_device['model']}\nBOT_TOKEN = {bot_token}"

    with open(Path("./.env"), "w") as env_file:
        env_file.write(env_data)


def create_ini_file() -> None:
    api_key = token_hex(16)
    ini_data = f"[Settings]\nstart_time = 00\nend_time = 00\ncooldown_ceil = 1\ncommand_cooldown = 60\nlogging_level = 0\nuse_server = false\nserver_port = 5000\napi_key = {api_key}"

    with open(Path("./config.ini"), "w") as config_file:
        config_file.write(ini_data)


def main() -> None:
    api_key, bot_token = get_tokens()
    filtered_devices = get_devices(api_key)

    if not filtered_devices:
        print(
            "No devices associated to your API key found... Please make sure your light is properly set up, or address error messages if you have any. PROGRAM TERMINATING..."
        )
        return

    elif len(filtered_devices) > 1:
        chosen_device = list_devices(filtered_devices)

    else:
        print("Only one device found, it has been automatically chosen.")
        chosen_device = filtered_devices[0]

    while chosen_device == None:
        print("Invalid selection, please try again.")
        chosen_device = list_devices(filtered_devices)

    create_env_file(api_key, bot_token, chosen_device)
    create_ini_file()

    print(
        textwrap.dedent(
            """
            DISCLAIMER: PLEASE DO NOT SHARE YOUR GOVEE API KEY, DISCORD BOT TOKEN,
            OR YOUR .ENV FILE WITH ANYONE. I AM NOT RESPONSIBLE FOR ANYTHING THAT
            HAPPENS AFTER BREACHING THIS DISCLAIMER.
            """
        )
    )
    print('.env and config files created and setup is complete. Please run "main.py" to begin.')


if __name__ == "__main__":
    main()
