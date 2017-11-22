"""Test the callback functions and wrappers."""
from celery_slack.callbacks import slack_task_prerun
from celery_slack.callbacks import slack_task_failure
from celery_slack.callbacks import slack_task_success
from celery_slack.callbacks import slack_celery_startup
from celery_slack.callbacks import slack_celery_shutdown
from celery_slack.callbacks import slack_beat_init
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
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')
    slack_beat_init(**options)
    assert mocked_post_to_slack.called


def test_slack_celery_startup_callback(
        default_options,
        webhook,
        mocker,
        ):
    """Test the slack beat init callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')
    slack_celery_startup(**options)
    assert mocked_post_to_slack.called


def test_slack_celery_shutdown_callback(
        default_options,
        webhook,
        mocker,
        ):
    """Test the slack beat init callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')
    slack_celery_shutdown(**options)
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
    """Test the slack beat init callback."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("task_id")
    these_options.pop("task")
    these_options.pop("args")
    these_options.pop("kwargs")
    these_options.pop("mocker")
    options = get_options(default_options, **these_options)
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')
    slack_task_prerun(task_id, task, args, kwargs, **options)
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
    """Test the slack beat init callback."""
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
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')

    class CallbackTester(object):
        def __init__(self):
            self.name = task_name

        @slack_task_success(**options)
        def callback(self, retval, task_id, args, kwargs):
            pass

    # need prerun for stopwatch
    slack_task_prerun(task_id, task, args, kwargs, **options)

    cbt = CallbackTester()
    cbt.callback(retval, task_id, args, kwargs)

    if ((exclude_tasks and task_name in exclude_tasks) or
            (include_tasks and task_name not in include_tasks)):
        assert mocked_post_to_slack.call_count == 1
    else:
        assert mocked_post_to_slack.call_count == 2


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
    """Test the slack beat init callback."""
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
    mocked_post_to_slack = mocker.patch('celery_slack.callbacks.post_to_slack')

    class CallbackTester(object):
        def __init__(self):
            self.name = task_name

        @slack_task_failure(**options)
        def callback(self, exc, task_id, args, kwargs, einfo):
            pass

    # need prerun for stopwatch
    slack_task_prerun(task_id, task, args, kwargs, **options)

    cbt = CallbackTester()
    cbt.callback(exc, task_id, args, kwargs, einfo)

    if ((exclude_tasks and task_name in exclude_tasks) or
            (include_tasks and task_name not in include_tasks)):
        assert mocked_post_to_slack.call_count == 1
    else:
        assert mocked_post_to_slack.call_count == 2
