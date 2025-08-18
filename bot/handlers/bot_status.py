from enum import Enum


class BotStatus(str, Enum):
    """Enum for bot status."""

    IGNORED = "ignored"
    OK = "ok"
