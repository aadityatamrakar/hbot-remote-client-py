from flask import Flask, request
from hbotrc import BotCommands
import json

app = Flask(__name__)
clients = {}


@app.route("/<instance_id>/<command>", methods=["POST"])
def execute_command(instance_id, command):
    params = request.get_json()

    print(f"[*] Instance ID: {instance_id}")
    print(f"[*] Command: {command}")
    print(f"[*] Params: {params}")

    if instance_id not in clients:
        clients[instance_id] = BotCommands(
            host="localhost",
            port=1883,
            username="",
            password="",
            bot_id=instance_id,
        )

    if command == "stop":
        resp = clients[instance_id].stop(**params)
        json_resp = {"status": resp.status, "msg": resp.msg}
    elif command == "start":
        resp = clients[instance_id].start(**params)
        json_resp = {"status": resp.status, "msg": resp.msg}
    elif command == "import":
        resp = clients[instance_id].import_strategy(**params)
        json_resp = {"status": resp.status, "msg": resp.msg}
    elif command == "config":
        resp = clients[instance_id].config(**params)
        json_resp = {
            "status": resp.status,
            "msg": resp.msg,
            "changes": resp.changes,
            "config": resp.config,
        }
    elif command == "status":
        resp = clients[instance_id].status(**params)
        json_resp = {"status": resp.status, "msg": resp.msg}

    print(f"[*] Response -> {resp}")
    return json.dumps(json_resp)


if __name__ == "__main__":
    app.run(debug=True)
