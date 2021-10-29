import json

from flask import Flask
from typing import Any, Dict

from app import blueprints
from app.shared.mongodb import mongo


def _initialize_app(config: Dict[str, Any]) -> Flask:
    app: Flask = Flask(__name__)
    app.config.update(config)
    blueprints.register_to(app)
    mongo.init_app(app)
    return app


with open('config.json', 'r') as config_handle:
    config: Dict[str, Any] = json.load(config_handle)
    app: Flask = _initialize_app(config)
