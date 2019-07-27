"""Slackify celery."""
import re

from celery.signals import beat_init
from celery.signals import celeryd_init
from celery.signals import task_prerun
from celery.signals import worker_shutdown
import kombu

from .callbacks import slack_beat_init
from .callbacks import slack_broker_connect
from .callbacks import slack_broker_disconnect
from .callbacks import slack_celery_shutdown
from .callbacks import slack_celery_startup
from .callbacks import slack_task_failure
from .callbacks import slack_task_prerun
from .callbacks import slack_task_success
from .exceptions import InvalidColorException
from .exceptions import MissingWebhookException
from .exceptions import TaskFiltrationException
from celery_slack import slack


DEFAULT_OPTIONS = {
    "slack_beat_init_color": "#FFCC2B",
    "slack_broker_connect_color": "#36A64F",
    "slack_broker_disconnect_color": "#D00001",
    "slack_celery_startup_color": "#FFCC2B",
    "slack_celery_shutdown_color": "#660033",
    "slack_task_prerun_color": "#D3D3D3",
    "slack_task_success_color": "#36A64F",
    "slack_task_failure_color": "#D00001",
    "slack_task_duplicate_color": "#DCDCDC",
    "slack_request_timeout": 1,
    "flower_base_url": None,
    "show_celery_hostname": False,
    "show_task_id": True,
    "show_task_execution_time": True,
    "show_task_args": True,
    "show_task_kwargs": True,
    "show_task_exception_info": True,
    "show_task_return_value": True,
    "show_task_prerun": False,
    "show_startup": True,
    "show_shutdown": True,
    "show_beat": True,
    "show_broker": False,
    "use_fixed_width": True,
    "include_tasks": None,
    "exclude_tasks": None,
    "failures_only": False,
    "webhook": None,
    "beat_schedule": None,
    "beat_show_full_task_path": False,
    "channel": "#alerts-celery", 
    "username": "celery",
    "default_emoji": ":celery:",
    "success_emoji": ":check_green:",
    "failure_emoji": ":red_circle:"
}

COLOR_REGEX = r"^#[a-fA-F0-9]{6}$"


class Slackify(object):
    """Add slack callbacks to celery signals.

    :param app: An instantiation of a celery.Celery object.
    :param slack_webhook: The webhook for the slack channel in which to post.
    """

    def __init__(self, app, webhook=None, beat_schedule=None, **options):
        """Slackify the celery object."""
        self.app = app
        self.options = DEFAULT_OPTIONS.copy()
        self.options.update(**options)
        self.options["webhook"] = webhook
        self.options["beat_schedule"] = (
            beat_schedule or self.options["beat_schedule"]
        )

        if self.options["webhook"] is None:
            raise MissingWebhookException("Slack webhook must be provided.")

        if self.options["include_tasks"] and self.options["exclude_tasks"]:
            raise TaskFiltrationException(
                "Only one of 'include_tasks' and 'exclude_tasks' "
                "options can be provided.")

        colors = [self.options[c] for c in self.options.keys() if "color" in c]
        for color in colors:
            if not re.search(COLOR_REGEX, color):
                raise InvalidColorException(
                    "Color options must be hex colors.")

        self._connect_signals()
        self._decorate_task_methods()
        self._decorate_kombu_retry()

        slack.TIMEOUT = self.options["slack_request_timeout"]

    def _connect_signals(self):
        """Connect callbacks to celery signals.

        Since we are creating partials here, the weak arg must be False.
        """
        # Beat
        if self.options["show_beat"]:
            beat_init.connect(
                slack_beat_init(**self.options),
                weak=False
            )

        # Celery
        if self.options["show_startup"]:
            celeryd_init.connect(
                slack_celery_startup(**self.options),
                weak=False
            )
        if self.options["show_shutdown"]:
            worker_shutdown.connect(
                slack_celery_shutdown(**self.options),
                weak=False
            )

        # Task
        task_prerun.connect(
            slack_task_prerun(**self.options),
            weak=False
        )

    def _decorate_task_methods(self):
        """Decorate the Task class result methods."""
        if not self.options["failures_only"]:
            self.app.Task.on_success = \
                slack_task_success(**self.options)(self.app.Task.on_success)
        self.app.Task.on_failure = \
            slack_task_failure(**self.options)(self.app.Task.on_failure)

    def _decorate_kombu_retry(self):
        """Decorate the kombu.connection.retry_over_time function."""
        if self.options["show_broker"]:
            kombu.connection.retry_over_time = \
                slack_broker_disconnect(**self.options)(
                    kombu.connection.retry_over_time
                )
            kombu.connection.retry_over_time = \
                slack_broker_connect(**self.options)(
                    kombu.connection.retry_over_time
                )
