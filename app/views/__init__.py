import logging
from typing import List
from types import ModuleType

from flask import Flask, Blueprint

from app.views import root, auth, test

logger: logging.Logger = logging.getLogger(__name__)

__views_enabled: List[ModuleType] = [
    root, auth, test
]


def register_views(app: Flask) -> None:
    for view in __views_enabled:
        for module in view.__dict__.values():
            if isinstance(module, Blueprint):
                logger.debug('Registering blueprint: %s', repr(module))
                app.register_blueprint(module)
