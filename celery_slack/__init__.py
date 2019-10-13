"""Module level accessible objects."""
from ._version import __version__
from ._version import __description__
from ._version import __url__
from ._version import __title__
from ._version import __author__
from ._version import __author_email__
from ._version import __license__
from ._version import __copyright__
from ._version import __docs_copyright__
from .slackify import DEFAULT_OPTIONS
from .slackify import Slackify

__all__ = (
    Slackify,
    DEFAULT_OPTIONS,
    __version__,
    __description__,
    __url__,
    __title__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
    __docs_copyright__,
)
