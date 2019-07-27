"""Test the callback functions and wrappers."""
from unittest.mock import MagicMock
from celery_slack.callbacks import slack_task_prerun
from celery_slack.callbacks import slack_task_failure
from celery_slack.callbacks import slack_task_success
from celery_slack.callbacks import slack_celery_startup
from celery_slack.callbacks import slack_celery_shutdown
from celery_slack.callbacks import slack_beat_init
from celery_slack.callbacks import slack_broker_connect
from celery_slack.callbacks import slack_broker_disconnect
from celery_slack import callbacks
from .conftest import get_options


def test_slack_beat_init_callback(
        default_options,
        webhook,
        mocker,
        ):
    """Test the slack beat init callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")
    slack_beat_init(**options)()
    assert mocked_post_to_slack.called


def test_slack_celery_startup_callback(
        default_options,
        webhook,
        mocker,
        ):
    """Test the slack celery startup callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")
    slack_celery_startup(**options)()
    assert mocked_post_to_slack.called


def test_slack_celery_shutdown_callback(
        default_options,
        webhook,
        mocker,
        ):
    """Test the slack celery shutdown callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")
    slack_celery_shutdown(**options)()
    assert mocked_post_to_slack.called


def test_slack_task_prerun_callback(
        default_options,
        show_task_prerun,
        webhook,
        task_id,
        task,
        args,
        kwargs,
        mocker,
        ):
    """Test the slack task prerun callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("task_id")
    these_options.pop("task")
    these_options.pop("args")
    these_options.pop("kwargs")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")
    slack_task_prerun(**options)(task_id, task, args, kwargs)
    if show_task_prerun:
        assert mocked_post_to_slack.called
    else:
        assert not mocked_post_to_slack.called


def test_slack_task_success_callback(
        default_options,
        include_tasks,
        exclude_tasks,
        webhook,
        slack_attachment,
        retval,
        task_name,
        task,
        task_id,
        args,
        kwargs,
        mocker,
        ):
    """Test the slack task success callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    these_options.pop("retval")
    these_options.pop("task_name")
    these_options.pop("task")
    these_options.pop("task_id")
    these_options.pop("args")
    these_options.pop("kwargs")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")

    class CallbackTester(object):

        request = MagicMock()
        def __init__(self):
            self.name = task_name

        @slack_task_success(**options)
        def callback(self, retval, task_id, args, kwargs):
            pass

    # need prerun for stopwatch
    slack_task_prerun(**options)(task_id, task, args, kwargs)

    cbt = CallbackTester()
    cbt.callback(retval, task_id, args, kwargs)

    if ((exclude_tasks and task_name in exclude_tasks) or
            (include_tasks and task_name not in include_tasks)):
        assert mocked_post_to_slack.call_count == 0
    else:
        assert mocked_post_to_slack.call_count == 1


def test_slack_task_failure_callback(
        default_options,
        include_tasks,
        exclude_tasks,
        webhook,
        slack_attachment,
        retval,
        task_name,
        task,
        task_id,
        args,
        kwargs,
        exc,
        einfo,
        mocker,
        ):
    """Test the slack task failure callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    these_options.pop("retval")
    these_options.pop("task_name")
    these_options.pop("task")
    these_options.pop("task_id")
    these_options.pop("args")
    these_options.pop("exc")
    these_options.pop("einfo")
    these_options.pop("kwargs")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")

    class CallbackTester(object):

        request = MagicMock()

        def __init__(self):
            self.name = task_name

        @slack_task_failure(**options)
        def callback(self, exc, task_id, args, kwargs, einfo):
            pass

    # need prerun for stopwatch
    slack_task_prerun(**options)(task_id, task, args, kwargs)

    cbt = CallbackTester()
    cbt.callback(exc, task_id, args, kwargs, einfo)

    if ((exclude_tasks and task_name in exclude_tasks) or
            (include_tasks and task_name not in include_tasks)):
        assert mocked_post_to_slack.call_count == 0
    else:
        assert mocked_post_to_slack.call_count == 1


def test_slack_broker_connect_callback(
        default_options,
        broker_connected,
        mocker,
        ):
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")

    # Mock out internals of kombu.connection.retry_over_time
    def fun():
        pass

    catch = None

    def retry_over_time(fun, catch, args=[], kwargs={}, errback=None,
        max_retries=None, interval_start=2, interval_step=2,
        interval_max=30, callback=None):
        pass

    callbacks.BROKER_CONNECTED = broker_connected

    # Decorate
    retry_over_time = slack_broker_connect(**options)(retry_over_time)

    # Call
    retry_over_time(fun, catch)

    if broker_connected:
        assert not mocked_post_to_slack.called
    else:
        assert mocked_post_to_slack.called


def test_slack_broker_disconnect_callback(
        default_options,
        mocker,
        callback,
        ):
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    these_options.pop("callback")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch("celery_slack.callbacks.post_to_slack")

    # Mock out internals of kombu.connection.retry_over_time
    def fun():
        pass

    catch = None

    def retry_over_time(fun, catch, args=[], kwargs={}, errback=None,
        max_retries=None, interval_start=2, interval_step=2,
        interval_max=30, callback=None):
        # Must execute the callback assuming dicsonnection occurred
        if callback is not None:
            callback()

    # Force the cooldown expiry
    callbacks.BROKER_DISCONNECT_TIME = \
        callbacks.BROKER_DISCONNECT_TIME - callbacks.BROKER_COOLDOWN

    # Decorate
    retry_over_time = slack_broker_disconnect(**options)(retry_over_time)

    # Call
    retry_over_time(fun, catch, callback=callback)

    assert mocked_post_to_slack.called
