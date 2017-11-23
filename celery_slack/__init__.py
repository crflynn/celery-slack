"""Module level accessible objects."""
from .__version__ import __version__
from .__version__ import __description__
from .__version__ import __url__
from .__version__ import __title__
from .__version__ import __author__
from .__version__ import __author_email__
from .__version__ import __license__
from .__version__ import __copyright__
from .__version__ import __docs_copyright__
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
