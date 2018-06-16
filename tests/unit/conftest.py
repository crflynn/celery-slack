"""Pytest fixtures."""
# flake8: noqa
import copy
from datetime import timedelta
import os
import platform
import uuid

from celery import __version__ as CELERY_VERSION
from celery.schedules import crontab
if CELERY_VERSION >= "4.0.0":
    from celery.schedules import solar
import pytest

from celery_slack import DEFAULT_OPTIONS
from tests.celeryapp.schedule import get_schedule

# local or travis
try:
    from ..secret import slack_webhook
except Exception:
    slack_webhook = os.environ["SLACK_WEBHOOK"]


PYTHON_VERSION = platform.python_version()
PYTHON_VERSION_THRESHOLD = "3.4"

# Use vcrpy for python3.4 or higher, else use repsonses
if PYTHON_VERSION >= PYTHON_VERSION_THRESHOLD:
    import vcr
    CASSETTE_LIBRARY = "tests/cassettes"

    if not os.path.exists(CASSETTE_LIBRARY):
        os.makedirs(CASSETTE_LIBRARY)

    def scrub_login_request(request):
        """Remove webhooks from cassettes."""
        request.uri = "https://hooks.slack.com/services/SLACK_WEBHOOK"
        return request

    my_vcr = vcr.VCR(before_record_request=scrub_login_request)
    RECORDER = my_vcr

    @pytest.fixture
    def recorder():
        return RECORDER
else:
    @pytest.fixture
    def recorder():
        return None


@pytest.fixture
def default_options():
    return DEFAULT_OPTIONS


@pytest.fixture
def webhook():
    """Return test slack webhook."""
    return slack_webhook


@pytest.fixture(params=[slack_webhook, None])
def possible_webhook(request):
    """Return webhooks."""
    return request.param


@pytest.fixture(params=[
    {
        "attachments": [
            {
                "fallback": "sample message",
                "color": "#36A64F",
                "text": "*sample* _message_",
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    },
    None
])
def slack_attachment(request):
    """Return a test slack message attachment."""
    return request.param


@pytest.fixture(params=[
    crontab(hour=12, minute=12),
    solar("sunset", 50, 50) if CELERY_VERSION > "4.0.0" else 9000,
    timedelta(5),
    3000
])
def schedule(request):
    """Return all the schedule types."""
    return request.param


class ObjectWithStr(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name


class ObjectWithRepr(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name


class ObjectWithout(object):
    def __init__(self, name):
        self.name = name


@pytest.fixture(params=[
    {"return": "value"},
    "return value",
    ObjectWithStr("return value"),
    ObjectWithRepr("return value"),
    ObjectWithout("return value"),
])
def retval(request):
    """Return a fake retval."""
    return request.param


@pytest.fixture
def task_name():
    """Return a fake task_id."""
    return "task.name"


@pytest.fixture
def exc():
    """Return a fake task_id."""
    return "exception message"


@pytest.fixture
def einfo():
    """Return a fake task_id."""
    return "traceback message"


@pytest.fixture
def task_id():
    """Return a fake task_id."""
    return str(uuid.uuid4())


@pytest.fixture
def args():
    """Return a fake set of args."""
    return []


@pytest.fixture
def kwargs():
    """Return a fake set of kwargs."""
    return {}


class Task(object):
    """Fake task object."""

    def __init__(self, name):
        """Init."""
        self.name = name


@pytest.fixture
def task():
    """Return a fake task object."""
    return Task("task.name")


@pytest.fixture(params=[None, "https://flower.example.com"])
def flower_base_url(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_id(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_execution_time(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_celery_hostname(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_args(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_kwargs(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_exception_info(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_return_value(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_task_prerun(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_startup(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_shutdown(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_beat(request):
    return request.param


@pytest.fixture(params=[True, False])
def use_fixed_width(request):
    return request.param


@pytest.fixture(params=[None, ["task.name"], ["other"]])
def include_tasks(request):
    return request.param


@pytest.fixture(params=[None, ["task.name"], ["other"]])
def exclude_tasks(request):
    return request.param


@pytest.fixture(params=[True, False])
def failures_only(request):
    return request.param


@pytest.fixture(params=[slack_webhook])
def webhook(request):
    return request.param


@pytest.fixture(params=[None, get_schedule()])
def beat_schedule(request):
    return request.param


@pytest.fixture(params=[True, False])
def beat_show_full_task_path(request):
    return request.param


@pytest.fixture(params=[True, False])
def show_broker(request):
    return request.param


@pytest.fixture(params=[True, False])
def broker_connected(request):
    return request.param


def get_options(default, **kwargs):
    """Get full options dict."""
    options = copy.deepcopy(default)
    options.update(**kwargs)
    return dict(options)


class MockProcess(object):
    def __init__(self, name):
        self._name = name


@pytest.fixture(params=["MainProcess", "Beat", ""])
def process_name(request):
    return request.param


def mock_callback():
    pass

@pytest.fixture(params=[None, mock_callback])
def callback(request):
    return request.param
