import os
import yaml
import logging

from typing import Dict

from flask import Flask

from yaml import Loader
from yaml.scanner import ScannerError

from app.views import register_views
from app.shared.database import db

logger: logging.Logger = logging.getLogger(__name__)


def __apply_configs(app: Flask, base_dir: str, *conf_files: str) -> None:

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


def __create_application() -> Flask:

    app: Flask = Flask(__name__)

    env: str = app.config['ENV']
    env_path: str = os.path.join('config', 'environments', env)

    __apply_configs(app, 'config', 'defaults.yaml')
    __apply_configs(app, env_path, 'secrets.yaml', 'config.yaml')

    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT'],
        datefmt=app.config['DATE_FORMAT']
    )
    logger.info('Configuring application for environment: "%s".', app.env)

    logger.debug('Initializing database: %s', app.config["MONGODB_SETTINGS"])
    db.init_app(app)

    logger.debug('Registering views...')
    register_views(app)

    logger.debug('Application is now configured.')
    return app


app: Flask = __create_application()
