import logging

from datetime import datetime

from typing import Optional, Tuple

from mongoengine.queryset import QuerySet
from mongoengine.errors import NotUniqueError

from app.auth import crypto
from app.models.user import User

logger = logging.getLogger(__name__)


def create_user(
    username: str,
    password: str,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None
) -> bool:

    logger.debug('Creating new user object for username: "%s"', username)
    password_hash, password_salt = crypto.prepare_password(password)
    user_object: User = User(
        username=username,
        password_hash=password_hash,
        password_salt=password_salt,
        firstname=firstname,
        lastname=lastname,
        email=email,
        created=datetime.now(),
        last_seen=datetime.now()
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


def authenticate_user(username: str, password: str) -> Tuple[bool, str]:

    logging.debug('Attempting to authenticate user "%s"', username)

    if not (user_object := find_user(username)):
        logging.error('Login attempt failed with non-existent user: "%s"',
            username)
        return (False, 'User does not exist.')

    if user_object.locked:
        logging.warn('Authentication attempt with locked user: "%s"', username)
        return (False, 'Your account is locked. Contact an administrator.')

    logging.debug('Comparing password hashes for user "%s"', username)
    computed_password_hash, _ = crypto.prepare_password(
        password, user_object.password_salt)
    if user_object.password_hash == computed_password_hash:
        logging.info('Successful login with user: "%s"', username)
        return (True, 'Login successful.')

    logging.warn('Authentication failed with invalid credentials '
        ' for user "%s"', username)
    return (False, 'Invalid username or password.')
