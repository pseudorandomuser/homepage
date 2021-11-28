import os
import yaml
import logging
import importlib

from types import ModuleType
from typing import Dict, List

from flask.cli import AppGroup
from flask import Flask, Blueprint

from yaml import Loader
from yaml.scanner import ScannerError

from flask_mongoengine import MongoEngine

logger: logging.Logger = logging.getLogger(__name__)


def _load_config_files(
    app: Flask,
    config_paths: List[str]
) -> None:

    for config_path in config_paths:
        print(f'{__name__}: Loading configuration file: "{config_path}"')

        if not os.path.isfile(config_path):
            raise FileNotFoundError('Required configuration file is '
                f'missing: "{config_path}"')

        with open(config_path, 'r') as config_handle:
            try:
                config_map: Dict = yaml.load(config_handle, Loader=Loader)
                app.config.update(config_map)
            except ScannerError as error:
                raise error


def _register_components(
    app: Flask,
    modules: List[str]
) -> None:

    for module_name in modules:
        module_path: str = f'{__name__}.{module_name}'
        logger.debug('Attempting to load module <%s>', module_path)

        try:
            module: ModuleType = importlib.import_module(module_path)
        except ModuleNotFoundError as error:
            logger.error('Could not find enabled module <%s>', module_path)
            raise error

        for component in module.__dict__.values():

            if isinstance(component, Blueprint):
                logger.info('Registering blueprint %s from module <%s>',
                    repr(component), module_path)
                app.register_blueprint(component)

            elif isinstance(component, AppGroup):
                logger.info('Registering commands %s from module <%s>',
                    repr(component), module_path)
                app.cli.add_command(component)


def _create_application() -> Flask:

    app: Flask = Flask(__name__)

    env: str = app.config['ENV']

    config_root: str = 'instance'
    config_files_default: List[str] = ['defaults.yaml']
    config_files_env: List[str] = ['config.yaml', 'secrets.yaml']

    config_paths: List[str] = \
        [os.path.join(config_root, name) for name in config_files_default] + \
        [os.path.join(config_root, env, name) for name in config_files_env]
    _load_config_files(app, config_paths)

    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT'],
        datefmt=app.config['DATE_FORMAT']
    )
    logger.info('Configuring application for environment: "%s".', app.env)

    logger.debug('Initializing database: %s', app.config["MONGODB_SETTINGS"])
    database: MongoEngine = MongoEngine()
    database.init_app(app)

    logger.debug('Registering components...')
    enabled_modules: List[str] = app.config['MODULES']
    _register_components(app, enabled_modules)

    logger.debug('Application is now configured.')
    return app


app: Flask = _create_application()
