import requests
from json import dumps

colors_dict = {
    "off": (0, 0, 0),
    "on": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "lime": (191, 255, 0),
    "pink": (255, 182, 193),
    "turquoise": (64, 224, 208),
    "brown": (165, 42, 42),
    "teal": (0, 128, 128),
    "lavender": (230, 230, 250),
}


def colour_change_body(
    device_mac: str, model_num: str, colour: tuple = None, rgb: tuple = None
) -> dict | None:
    
    if colour:
        if colour not in colors_dict:
            return None
        
        elif colour == "off" or colour == "on":
            cmd = {"name": "turn", "value": colour}

        else:
            R, G, B = colors_dict[colour]
            cmd = {"name": "color", "value": {"r": R, "g": G, "b": B}}

    elif rgb:
        R, G, B = rgb

        if all(colour == 0 for colour in rgb):
            cmd = {"name": "turn", "value": "off"}
        else:
            cmd = {"name": "color", "value": {"r": R, "g": G, "b": B}}

    else:
        R, G, B = 255, 255, 255
        cmd = {"name": "color", "value": {"r": R, "g": G, "b": B}}

    request_body = {
        "device": device_mac,
        "model": model_num,
        "cmd": cmd,
    }

    return request_body


def brightness_change_body(device_mac: str, model_num: str, brightness: int) -> dict:
    request_body = {
        "device": device_mac,
        "model": model_num,
        "cmd": {"name": "brightness", "value": brightness},
    }

    return request_body


def PUT(api_key: str, request_body: dict) -> bool:
    params = {"Govee-API-Key": api_key, "Content-Type": "application/json"}

    request = requests.put(
        "https://developer-api.govee.com/v1/devices/control",
        headers=params,
        data=dumps(request_body),
        timeout=15
    )

    if request.status_code == 200:
        return True
    else:
        print(request.json())
        return False


def all_colours() -> list:
    return colors_dict.keys()
