"""Test Slackify."""
from celery import Celery
import pytest

from celery_slack import Slackify
from celery_slack.exceptions import MissingWebhookException
from celery_slack.exceptions import TaskFiltrationException
from celery_slack.exceptions import InvalidColorException
from .conftest import get_options


def test_slackify_webhook_exception(
        possible_webhook,
        default_options,
        ):
    """Test Slackify construction."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)
    options["webhook"] = possible_webhook

    # Test webhook exception
    if options["webhook"] is None:
        with pytest.raises(MissingWebhookException):
            app = Celery('schedule')
            app.config_from_object('tests.celeryapp.config')
            slack_app = Slackify(app, **options)
        return


def test_slackify_task_filtration_exception(
        webhook,
        include_tasks,
        exclude_tasks,
        default_options,
        ):
    """Test TaskFiltrationException."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)
    options["webhook"] = webhook

    if include_tasks and exclude_tasks:
        with pytest.raises(TaskFiltrationException):
            app = Celery('schedule')
            app.config_from_object('tests.celeryapp.config')
            slack_app = Slackify(app, **options)


def test_invalid_color_exception(webhook, default_options):
    """Test InvalidColorException."""
    options = get_options(default_options, **{})
    options["webhook"] = webhook

    options["slack_beat_init_color"] = 'asdf'
    with pytest.raises(InvalidColorException):
        app = Celery('schedule')
        app.config_from_object('tests.celeryapp.config')
        slack_app = Slackify(app, **options)

    # Doesn't raise with valid color.
    options["slack_beat_init_color"] = '#000000'
    slack_app = Slackify(app, **options)  # noqa F481


def test_failure_only_patching(webhook, failures_only, default_options):
    """Test failures_only option omits patching on_success method."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)

    app = Celery('schedule')
    app.config_from_object('tests.celeryapp.config')

    pre_patch_id = id(app.Task.on_success)
    slack_app = Slackify(app, **options)
    post_patch_id = id(app.Task.on_success)

    # If patching skipped ensure the method id is the same.
    if failures_only:
        assert pre_patch_id == post_patch_id
    else:
        assert pre_patch_id != post_patch_id
