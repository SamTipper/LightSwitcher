from flask import Flask, request, Response
from threading import Thread
from rx.subject import Subject
from json import dumps
from logger import Logger, LoggingLevel

app = Flask(__name__)

command_status_subject: Subject = Subject()
command_allowed = True
API_KEY = None # Will be set if server is being used
logger = None # Will be set if server is being used

### HELPER FUNCTIONS ###


def check_api_key(headers: dict) -> bool:
    if API_KEY == "0":
        return True

    elif not headers:
        logger.log("No headers sent in the request.", LoggingLevel.DEBUG)
        return False
    
    elif not headers['Authorization']:
        logger.log("No authorization header found in request.", LoggingLevel.DEBUG)
        return False
    
    elif headers['Authorization'] != API_KEY:
        logger.log(
            "Found authorization header but it came with the wrong API key.",
            LoggingLevel.DEBUG
        )
        return False
    
    else:
        return True
    

def generic_error(error) -> Response:
    logger.log("There was an error while toggling commands.", LoggingLevel.ERROR)

    return Response(
        response=dumps({
            "message": "There was an error while toggling commands.",
            "error": str(error)
        }),
        status=500,
        mimetype="application/json"
    )


def auth_error(error) -> Response:
    logger.log("There was an error during authorization.", LoggingLevel.ERROR)

    return Response(
        response=dumps({
            "message": "There was an error during authorization.",
            "error": str(error)
        }),
        status=403,
        mimetype="application/json"
    )


### END OF HELPER FUNCTIONS ### 


@app.route("/")
def home() -> str:
    return ""


@app.route("/toggle", methods=['GET'])
def toggle_commands() -> Response:
    try:
        global command_status_subject, command_allowed

        if not check_api_key(dict(request.headers)):
            return auth_error("Incorrect API key.")

        command_allowed = not command_allowed
        command_status_subject.on_next(command_allowed)
        logger.log(
            f"Light control toggled {'on' if command_allowed == True else 'off'}", 
            LoggingLevel.INFO
        )

        return Response(
            response=dumps({
                "status": "on" if command_allowed == True else "off"
            }),
            status=200,
            mimetype="application/json"
        )
   
    except Exception as e:
        return generic_error(e)


def run(port: int) -> None:
    app.run(host='0.0.0.0', port=port)
    print(f"Server running on http://{request.host}")
    logger.log(f"Flask server running on http://{request.host}", LoggingLevel.DEBUG)


def keep_alive(port: str, api_key: str, loggerInstance: Logger) -> None:
    if not port.strip().isdigit():
        logger.log(
            f"The \"server_port\" setting in the config.ini file is not a valid integer, please change it and try again.",
            LoggingLevel.CRITICAL
        )
        raise RuntimeError(
            "The \"server_port\" setting in the config.ini file is not a valid integer, please change it and try again."
        )

    try:
        global API_KEY, logger
        API_KEY = api_key.strip()
        logger = loggerInstance
        port = int(port)

        logger.log("Starting Flask server.", LoggingLevel.DEBUG)
        app_thread = Thread(target=run, args=(port,))
        app_thread.daemon = True
        app_thread.start()
        logger.log("Flask server started.", LoggingLevel.DEBUG)

    except Exception as e:
        logger.log(f"Tried to start the Flask API but failed, {e}", LoggingLevel.CRITICAL)

