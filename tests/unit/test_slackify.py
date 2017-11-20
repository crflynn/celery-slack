"""Test Slackify."""
import pytest

from celery_slack import Slackify
from celery_slack import DEFAULT_OPTIONS
from celery_slack.exceptions import MissingWebhookException
from celery_slack.exceptions import TaskFiltrationException
from celery_slack.exceptions import InvalidColorException
from .common import get_options
from ..celery.celery import app


def test_slackify(
        possible_webhook,
        include_tasks,
        exclude_tasks,
        failures_only,
        ):
    """Test Slackify construction."""
    these_options = locals()
    options = get_options(DEFAULT_OPTIONS, **these_options)
    options["webhook"] = possible_webhook
    print(possible_webhook)
    if options["webhook"] is None:
        with pytest.raises(MissingWebhookException):
            slack_app = Slackify(app, **options)
    elif include_tasks and exclude_tasks:
        with pytest.raises(TaskFiltrationException):
            slack_app = Slackify(app, **options)
    else:
        options["slack_beat_init_color"] = 'asdf'
        with pytest.raises(InvalidColorException):
            slack_app = Slackify(app, **options)

        options["slack_beat_init_color"] = '#000000'
        slack_app = Slackify(app, **options)
