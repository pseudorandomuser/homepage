import click
import logging

from typing import Optional

from flask.cli import AppGroup

from homepage.models.user import User
from homepage.auth.users import (
    create_user,
    delete_user,
    change_password,
    authenticate_user
)

cli = AppGroup('users')

logger = logging.getLogger(__name__)


@cli.command('create')
@click.argument('username')
@click.argument('password')
@click.argument('role', required=False)
def create(
    username: str,
    password: str,
    role: Optional[int] = None
) -> bool:
    return create_user(username, password, role=role)


@cli.command('delete')
@click.argument('username')
def delete(username: str) -> bool:
    return delete_user(username)


@cli.command('passwd')
@click.argument('username')
@click.argument('password')
def passwd(username: str, password: str) -> bool:
    return change_password(username, password)


@cli.command('auth')
@click.argument('username')
@click.argument('password')
def auth(username: str, password: str) -> User:
    return authenticate_user(username, password)
