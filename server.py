from flask import Flask, request, Response
from threading import Thread
from rx.subject import Subject
from json import dumps

app = Flask(__name__)

command_status_subject: Subject = Subject()
command_allowed = True


@app.route("/")
def home() -> str:
    return ""


@app.route("/toggle", methods=['GET'])
def toggle_commands() -> Response:
    try:
        global command_status_subject, command_allowed
        command_allowed = not command_allowed
        command_status_subject.on_next(command_allowed)
        
        return Response(
            response=dumps({
                "status": "on" if command_allowed == True else "off"
            }),
            status=200,
            mimetype="application/json"
        )
   
    except Exception as e:
        print(e)
        return Response(
            response=dumps({
                "message": "There was an error while toggling commands",
                "error": str(e)
            }),
            status=500,
            mimetype="application/json"
        )


def run() -> None:
  app.run(host='0.0.0.0', port=21435)
  print(f"Server running on http://{request.host}")


def keep_alive() -> None:
    try:
        app_thread = Thread(target=run)
        app_thread.daemon = True
        app_thread.start()

    except Exception as e:
        print("Tried to start API but failed", e)
