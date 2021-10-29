from flask import Flask, Blueprint
from typing import List

from app.views import root, auth, test

_blueprints: List[Blueprint] = [
    root.app, auth.app, test.app
]


def register_to(app: Flask) -> None:
    for blueprint in _blueprints:
        app.register_blueprint(blueprint)
