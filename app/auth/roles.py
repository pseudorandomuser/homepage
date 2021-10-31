from enum import IntEnum


class Role(IntEnum):
    UNPRIVILEGED: int = 0
    STANDARD: int = 10
    MODERATOR: int = 20
    ADMINISTRATOR: int = 30
    ROOT: int = 100
