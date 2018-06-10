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


def test_failure_only_patching(webhook, failures_only,
                               default_options, mocker):
    """Test failures_only option omits patching on_success method."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)

    app = Celery('schedule')
    app.config_from_object('tests.celeryapp.config')

    mocked_task_success = \
        mocker.patch('celery_slack.slackify.slack_task_success')

    slack_app = Slackify(app, **options)

    # If patching skipped ensure the method id is the same.
    if failures_only:
        assert not mocked_task_success.called
    else:
        assert mocked_task_success.called


def test_show_beat_option(webhook, show_beat, default_options, mocker):
    """Test the show_startup option."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)

    app = Celery('schedule')
    app.config_from_object('tests.celeryapp.config')

    mocked_slack_beat_init = \
        mocker.patch('celery_slack.slackify.slack_beat_init')

    slack_app = Slackify(app, **options)

    if show_beat:
        assert mocked_slack_beat_init.called
    else:
        assert not mocked_slack_beat_init.called


def test_show_startup_option(webhook, show_startup, default_options, mocker):
    """Test the show_startup option."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)

    app = Celery('schedule')
    app.config_from_object('tests.celeryapp.config')

    mocked_slack_celery_startup = \
        mocker.patch('celery_slack.slackify.slack_celery_startup')

    slack_app = Slackify(app, **options)

    if show_startup:
        assert mocked_slack_celery_startup.called
    else:
        assert not mocked_slack_celery_startup.called


def test_show_shutdown_option(webhook, show_shutdown, default_options, mocker):
    """Test the show_startup option."""
    these_options = locals()
    these_options.pop('default_options')
    options = get_options(default_options, **these_options)

    app = Celery('schedule')
    app.config_from_object('tests.celeryapp.config')

    mocked_slack_celery_shutdown = \
        mocker.patch('celery_slack.slackify.slack_celery_shutdown')

    slack_app = Slackify(app, **options)

    if show_shutdown:
        assert mocked_slack_celery_shutdown.called
    else:
        assert not mocked_slack_celery_shutdown.called
