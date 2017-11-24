"""Test slack functions."""
import socket

from celery_slack.attachments import add_task_to_stopwatch
from celery_slack.attachments import get_beat_init_attachment
from celery_slack.attachments import get_celery_shutdown_attachment
from celery_slack.attachments import get_celery_startup_attachment
from celery_slack.attachments import get_task_failure_attachment
from celery_slack.attachments import get_task_prerun_attachment
from celery_slack.attachments import get_task_success_attachment
from celery_slack.attachments import schedule_to_string
from .conftest import get_options


def test_schedule_to_string(schedule):
    """Test all types of schedules to string."""
    assert isinstance(schedule_to_string(schedule), str)


def test_beat_init_attachment(
        default_options,
        # flower_base_url,
        # show_task_id,
        # show_task_execution_time,
        show_celery_hostname,
        # show_task_args,
        # show_task_kwargs,
        # show_task_exception_info,
        # show_task_return_value,
        # show_task_prerun,
        use_fixed_width,
        # include_tasks,
        # exclude_tasks,
        # failures_only,
        # webhook,
        beat_schedule,
        beat_show_full_task_path,
        ):
    """Test the beat init attachments."""
    these_options = locals()
    these_options.pop("default_options")
    options = get_options(default_options, **these_options)
    attachment = get_beat_init_attachment(**options)

    message = attachment["attachments"][0]["text"]

    if show_celery_hostname:
        assert socket.gethostname() in message
    else:
        assert socket.gethostname() not in message
    if beat_schedule:
        assert "with schedule" in message
        if use_fixed_width:
            assert "`" in message
        if beat_show_full_task_path:
            assert "tests.celery.tasks.successful_task " in message
        else:
            assert "tests.celery.tasks.successful_task " not in message
            assert "tasks.successful_task" in message
    else:
        assert "with schedule" not in message


def test_celery_startup_attachment(
        default_options,
        # flower_base_url,
        # show_task_id,
        # show_task_execution_time,
        show_celery_hostname,
        # show_task_args,
        # show_task_kwargs,
        # show_task_exception_info,
        # show_task_return_value,
        # show_task_prerun,
        # use_fixed_width,
        # include_tasks,
        # exclude_tasks,
        # failures_only,
        # webhook,
        # beat_schedule,
        # beat_show_full_task_path,
        ):
    """Test the celery startup attachment."""
    these_options = locals()
    these_options.pop("default_options")
    options = get_options(default_options, **these_options)
    attachment = get_celery_startup_attachment(**options)

    message = attachment["attachments"][0]["text"]

    if show_celery_hostname:
        assert socket.gethostname() in message
    else:
        assert socket.gethostname() not in message


def test_celery_shutdown_attachment(
        default_options,
        # flower_base_url,
        # show_task_id,
        # show_task_execution_time,
        show_celery_hostname,
        # show_task_args,
        # show_task_kwargs,
        # show_task_exception_info,
        # show_task_return_value,
        # show_task_prerun,
        # use_fixed_width,
        # include_tasks,
        # exclude_tasks,
        # failures_only,
        # webhook,
        # beat_schedule,
        # beat_show_full_task_path,
        ):
    """Test the celery shutdown attachment."""
    these_options = locals()
    these_options.pop("default_options")
    options = get_options(default_options, **these_options)
    attachment = get_celery_shutdown_attachment(**options)

    message = attachment["attachments"][0]["text"]

    if show_celery_hostname:
        assert socket.gethostname() in message
    else:
        assert socket.gethostname() not in message


def test_task_prerun_attachment(
        default_options,
        flower_base_url,
        show_task_id,
        # show_task_execution_time,
        # show_celery_hostname,
        show_task_args,
        show_task_kwargs,
        # show_task_exception_info,
        # show_task_return_value,
        # show_task_prerun,
        use_fixed_width,
        # include_tasks,
        # exclude_tasks,
        # failures_only,
        # webhook,
        # beat_schedule,
        # beat_show_full_task_path,
        task_id,
        task,
        args,
        kwargs
        ):
    """Test the task prerun attachment."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("task_id")
    these_options.pop("task")
    these_options.pop("args")
    these_options.pop("kwargs")
    options = get_options(default_options, **these_options)
    attachment = get_task_prerun_attachment(
        task_id, task, args, kwargs, **options)

    message = attachment["attachments"][0]["text"]
    title_link = attachment["attachments"][0].get("title_link", None)

    if flower_base_url:
        assert flower_base_url in title_link
    else:
        assert title_link is None
    if show_task_id:
        assert "Task ID" in message
    else:
        assert "Task ID" not in message
    if show_task_args:
        assert "args" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    if show_task_kwargs:
        assert "kwargs" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    else:
        assert "kwargs" not in message


def test_task_failure_attachment(
        default_options,
        flower_base_url,
        show_task_id,
        show_task_execution_time,
        # show_celery_hostname,
        show_task_args,
        show_task_kwargs,
        show_task_exception_info,
        # show_task_return_value,
        # show_task_prerun,
        use_fixed_width,
        include_tasks,
        exclude_tasks,
        # failures_only,
        # webhook,
        # beat_schedule,
        # beat_show_full_task_path,
        task_name,
        exc,
        task_id,
        args,
        kwargs,
        einfo
        ):
    """Test the task failure attachment."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("task_name")
    these_options.pop("exc")
    these_options.pop("task_id")
    these_options.pop("args")
    these_options.pop("kwargs")
    these_options.pop("einfo")
    add_task_to_stopwatch(task_id)
    options = get_options(default_options, **these_options)

    if bool(include_tasks) ^ bool(exclude_tasks):
        attachment = get_task_failure_attachment(
            task_name, exc, task_id, args, kwargs, einfo, **options)
    else:
        return

    if attachment is None:
        if include_tasks is not None:
            assert task_name not in include_tasks
        if exclude_tasks is not None:
            assert task_name in exclude_tasks
        return

    message = attachment["attachments"][0]["text"]
    title_link = attachment["attachments"][0].get("title_link", None)

    if flower_base_url:
        assert flower_base_url in title_link
    else:
        assert title_link is None
    if show_task_id:
        assert "Task ID" in message
    else:
        assert "Task ID" not in message
    if show_task_execution_time:
        assert "Execution time" in message
    else:
        assert "Execution time" not in message
    if show_task_args:
        assert "args" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    if show_task_kwargs:
        assert "kwargs" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    else:
        assert "kwargs" not in message
    if show_task_exception_info:
        assert "Info" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    else:
        assert "Info" not in message


def test_task_success_attachment(
        default_options,
        flower_base_url,
        show_task_id,
        show_task_execution_time,
        # show_celery_hostname,
        show_task_args,
        show_task_kwargs,
        # show_task_exception_info,
        show_task_return_value,
        # show_task_prerun,
        use_fixed_width,
        include_tasks,
        exclude_tasks,
        # failures_only,
        # webhook,
        # beat_schedule,
        # beat_show_full_task_path,
        task_name,
        retval,
        task_id,
        args,
        kwargs
        ):
    """Test the task success attachment."""
    these_options = locals()
    these_options.pop("default_options")
    these_options.pop("task_name")
    these_options.pop("retval")
    these_options.pop("task_id")
    these_options.pop("args")
    these_options.pop("kwargs")
    add_task_to_stopwatch(task_id)
    options = get_options(default_options, **these_options)

    if bool(include_tasks) ^ bool(exclude_tasks):
        attachment = get_task_success_attachment(
            task_name, retval, task_id, args, kwargs, **options)
    else:
        return

    if attachment is None:
        if include_tasks is not None:
            assert task_name not in include_tasks
        if exclude_tasks is not None:
            assert task_name in exclude_tasks
        return

    message = attachment["attachments"][0]["text"]
    title_link = attachment["attachments"][0].get("title_link", None)

    if flower_base_url:
        assert flower_base_url in title_link
    else:
        assert title_link is None
    if show_task_id:
        assert "Task ID" in message
    else:
        assert "Task ID" not in message
    if show_task_execution_time:
        assert "Execution time" in message
    else:
        assert "Execution time" not in message
    if show_task_args:
        assert "args" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    if show_task_kwargs:
        assert "kwargs" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    else:
        assert "kwargs" not in message
    if show_task_return_value:
        assert "Return" in message
        if use_fixed_width:
            assert "`" in message
        else:
            assert "`" not in message
    else:
        assert "Return" not in message
