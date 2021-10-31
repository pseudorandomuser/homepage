import click
from flask.cli import AppGroup

from app.auth import users

cli = AppGroup(__name__)


@cli.command('create-user')
@click.argument('username')
@click.argument('password')
def create_user(username: str, password: str) -> bool:
    return users.create_user(username, password)
