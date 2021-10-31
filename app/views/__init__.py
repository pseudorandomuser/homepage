import logging
import importlib

from typing import List
from types import ModuleType

from flask import Flask
from flask.blueprints import Blueprint

logger: logging.Logger = logging.getLogger(__name__)


def register_views(app: Flask) -> None:

    view_names: List[str] = app.config['VIEWS']
    for view_name in view_names:
        module_name: str = f'{__name__}.{view_name}'
        logger.debug('Attempting to load view "%s" from module <%s>',
            view_name, module_name)

        try:
            view: ModuleType = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            logger.error('Could not find module <%s> for view "%s"',
                module_name, view_name)
            raise error

        for submodule in view.__dict__.values():
            if isinstance(submodule, Blueprint):
                logger.info('Registering blueprint: %s', repr(submodule))
                app.register_blueprint(submodule)
