import click
import logging

from typing import Optional

from flask.cli import AppGroup

from app.auth import users

cli = AppGroup(__name__)

logger = logging.getLogger(__name__)


@cli.command('create-user')
@click.argument('username')
@click.argument('password')
@click.argument('role', required=False)
def create_user(
    username: str,
    password: str,
    role: Optional[int] = None
) -> bool:
    return users.create_user(username, password, role=role)


@cli.command('delete-user')
@click.argument('username')
def delete_user(username: str) -> bool:
    return users.delete_user(username)


@cli.command('change-password')
@click.argument('username')
@click.argument('password')
def change_password(username: str, password: str) -> bool:
    return users.change_password(username, password)
