import logging

from typing import Optional
from datetime import datetime

from mongoengine.queryset import QuerySet
from mongoengine.errors import NotUniqueError, OperationError

from homepage.auth import crypto
from homepage.models.user import User

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def create_user(
    username: str,
    password: str,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[int] = None
) -> bool:

    logger.debug('Creating new user object for username: "%s"', username)
    password_hash, password_salt = crypto.prepare_password(password)

    user_object: User = User(
        username=username,
        password_hash=password_hash,
        password_salt=password_salt,
        created=datetime.now(),
        last_login=datetime.now(),
        firstname=firstname,
        lastname=lastname,
        email=email,
        role=role
    )

    try:
        user_object.validate()
        user_object.save()
        logger.info('Successfully created new user: "%s"', username)
        return True

    except NotUniqueError:
        logger.warn('Could not create user "%s" because it already exists',
            username)
        return False

    except Exception as exception:
        logger.error('Could not create user "%s" because of an error: "%s"',
            username, str(exception))
        return False


def find_user(username: str) -> Optional[User]:

    logger.debug('Querying database for user "%s"', username)
    user_objects: QuerySet = User.objects(username=username)

    if user_objects.count() == 1:
        logger.debug('Found entry for user "%s" in database', username)
        return user_objects.first()

    logger.debug('Could not find entry for user "%s" in database', username)
    return None


def delete_user(username: str) -> bool:

    if not (user_object := find_user(username)):
        logging.error('User deletion failed with non-existent user: "%s"',
            username)
        return False

    try:
        user_object.delete()
        logging.info('User "%s" deleted', username)
        return True

    except OperationError as error:
        logging.error('User deletion failed for user "%s": %s',
            username, str(error))
        return False


def change_password(username: str, password: str) -> bool:

    if not (user_object := find_user(username)):
        logging.error('Password change failed with non-existent user: "%s"',
            username)
        return False

    try:
        user_object.password_hash, user_object.password_salt = \
            crypto.prepare_password(password)
        user_object.save()
        logging.info('Password changed for user "%s"', username)
        return True

    except OperationError as error:
        logging.error('Password change failed for user "%s": %s',
            username, str(error))
        return False


def authenticate_user(
    username: str,
    password: str
) -> User:

    logging.debug('Attempting to authenticate user "%s"', username)

    if not (user_object := find_user(username)):
        logging.error('Login attempt failed with non-existent user: "%s"',
            username)
        raise AuthenticationError('User does not exist.')

    if user_object.locked:
        logging.warn('Authentication attempt with locked user: "%s"', username)
        raise AuthenticationError('Your account is locked. '
            'Contact an administrator.')

    logging.debug('Comparing password hashes for user "%s"', username)
    computed_password_hash, _ = crypto.prepare_password(
        password, user_object.password_salt)

    if user_object.password_hash == computed_password_hash:
        user_object.last_login = datetime.now()
        user_object.save()
        logging.info('Successful login with user: "%s"', username)
        return user_object

    logging.warn('Authentication failed with invalid credentials '
        'for user "%s"', username)
    raise AuthenticationError('Invalid username or password.')
