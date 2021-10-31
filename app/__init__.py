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


def __apply_configs(
    app: Flask,
    base_dir: str,
    *conf_files: str
) -> None:

    for conf_file in conf_files:
        conf_path: str = os.path.join(base_dir, conf_file)
        print(f'{__name__}: Loading configuration file: "{conf_path}"')

        if not os.path.isfile(conf_path):
            raise FileNotFoundError('Required configuration file is '
                f'missing: "{conf_path}"')

        with open(conf_path, 'r') as conf_handle:
            try:
                conf_map: Dict = yaml.load(conf_handle, Loader=Loader)
                app.config.update(conf_map)
            except ScannerError as error:
                raise error


def __register_components(
    app: Flask,
    root_module: str,
    submodules: List[str]
) -> None:

    for module_name in submodules:
        module_path: str = f'{__name__}.{root_module}.{module_name}'
        logger.debug('Attempting to load module <%s>', module_path)

        try:
            module: ModuleType = importlib.import_module(module_path)
        except ModuleNotFoundError as error:
            logger.error('Could not find module <%s>', module_path)
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


def __create_application() -> Flask:

    app: Flask = Flask(__name__)

    env: str = app.config['ENV']

    conf_path: str = 'config'
    env_path: str = os.path.join(conf_path, 'environments', env)

    __apply_configs(app, conf_path, 'defaults.yaml')
    __apply_configs(app, env_path, 'secrets.yaml', 'config.yaml')

    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT'],
        datefmt=app.config['DATE_FORMAT']
    )
    logger.info('Configuring application for environment: "%s".', app.env)

    logger.debug('Initializing database: %s', app.config["MONGODB_SETTINGS"])
    database: MongoEngine = MongoEngine()
    database.init_app(app)

    logger.debug('Registering views...')
    enabled_views: List[str] = app.config['VIEWS']
    __register_components(app, 'views', enabled_views)

    logger.debug('Registering commands...')
    enabled_commands: List[str] = app.config['COMMANDS']
    __register_components(app, 'commands', enabled_commands)

    logger.debug('Application is now configured.')
    return app


app: Flask = __create_application()
