"""Local mock server for testing the admin UI."""
from __future__ import annotations

import json
import pathlib
from typing import Dict

from flask import Flask, Response, request, send_from_directory

BASE_DIR = pathlib.Path(__file__).parent
STATE_FILE = BASE_DIR / "mock_state.json"
DEFAULT_STATE = {
    "config": "BarMachine;12345678",
    "ingredients": "rum;Ром\npnpljc;Ананасовый сок\nvdk;Водка",
    "recipes": "Пина колада;rum(60),pnpljc(180)\nРомовый сплеш;rum(50)",
    "pumps": "rum;0\npnpljc;1\nvdk;-1",
}

app = Flask(__name__, static_folder="web", static_url_path="")


def load_state() -> Dict[str, str]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return DEFAULT_STATE.copy()


def save_state(data: Dict[str, str]) -> None:
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_state_value(key: str) -> str:
    state = load_state()
    return state.get(key, "")


def update_state_value(key: str, value: str) -> None:
    state = load_state()
    state[key] = value
    save_state(state)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        update_state_value("config", request.data.decode("utf-8"))
        return ("OK", 200)
    return Response(get_state_value("config"), mimetype="text/plain")


@app.route("/ingredients", methods=["GET", "POST"])
def ingredients():
    if request.method == "POST":
        update_state_value("ingredients", request.data.decode("utf-8"))
        return ("OK", 200)
    return Response(get_state_value("ingredients"), mimetype="text/plain")


@app.route("/cocktail_recipes", methods=["GET", "POST"])
def cocktail_recipes():
    if request.method == "POST":
        update_state_value("recipes", request.data.decode("utf-8"))
        return ("OK", 200)
    return Response(get_state_value("recipes"), mimetype="text/plain")


@app.route("/pump_assigment", methods=["GET", "POST"])
def pump_assignment():
    if request.method == "POST":
        update_state_value("pumps", request.data.decode("utf-8"))
        return ("OK", 200)
    return Response(get_state_value("pumps"), mimetype="text/plain")


if __name__ == "__main__":
    print("Mock server available on http://127.0.0.1:5000")
    app.run(debug=True)
