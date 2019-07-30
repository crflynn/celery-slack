"""Slack attachment builders."""
from datetime import timedelta
import json
import re
import socket
import time

from billiard.process import current_process
from celery import __version__ as CELERY_VERSION
from celery.schedules import crontab

if CELERY_VERSION >= "4.0.0":
    from celery.schedules import solar


STOPWATCH = {}
BEAT_DELIMITER = " -> "


def add_task_to_stopwatch(task_id):
    """Add a task_id to the STOPWATCH dict."""
    if task_id not in STOPWATCH.keys():
        STOPWATCH[task_id] = time.time()
        return True


def get_task_prerun_attachment(task_id, task, args, kwargs, **cbkwargs):
    """Create the slack message attachment for a task prerun."""

    if (cbkwargs["exclude_tasks"] and
            any([re.search(task, task_name)
                for task in cbkwargs["exclude_tasks"]])):
        STOPWATCH.pop(task_id)
        return
    elif (cbkwargs["include_tasks"] and
            not any([re.search(task, task_name)
                    for task in cbkwargs["include_tasks"]])):
        STOPWATCH.pop(task_id)
        return
    
    message = "Executing -- " + task.name.rsplit(".", 1)[-1]

    lines = ["Name: *" + task.name + "*"]

    if cbkwargs["show_task_id"]:
        lines.append("Task ID: " + task_id)

    if cbkwargs["use_fixed_width"]:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + "`" + str(args) + "`")
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + "`" + str(kwargs) + "`")
    else:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + str(args))
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + str(kwargs))

    executing = "\n".join(lines)

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": cbkwargs["slack_task_prerun_color"],
                "text": executing,
                "title": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    if cbkwargs["flower_base_url"]:
        attachment["attachments"][0]["title_link"] = (
            cbkwargs["flower_base_url"] +
            "/task/{tid}".format(tid=task_id)
        )

    return attachment


def get_task_success_attachment(task_name, retval, task_id,
                                args, kwargs, **cbkwargs):
    """Create the slack message attachment for a task success."""
    if (cbkwargs["exclude_tasks"] and
            any([re.search(task, task_name)
                for task in cbkwargs["exclude_tasks"]])):
        STOPWATCH.pop(task_id)
        return
    elif (cbkwargs["include_tasks"] and
            not any([re.search(task, task_name)
                    for task in cbkwargs["include_tasks"]])):
        STOPWATCH.pop(task_id)
        return

    if isinstance(retval, dict):
        retval = json.dumps(retval, indent=4)
    else:
        retval = str(retval)

    message = "SUCCESS -- " + task_name.rsplit(".", 1)[-1]

    elapsed = divmod(time.time() - STOPWATCH.pop(task_id), 60)

    lines = ["Name: *" + task_name + "*"]

    if cbkwargs["show_task_execution_time"]:
        lines.append("Execution time: {m} minutes {s} seconds".format(
            m=str(int(elapsed[0])),
            s=str(int(elapsed[1])),
        ))
    if cbkwargs["show_task_id"]:
        lines.append("Task ID: " + task_id)

    if cbkwargs["use_fixed_width"]:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + "`" + str(args) + "`")
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + "`" + str(kwargs) + "`")
        if cbkwargs["show_task_return_value"]:
            lines.append("Returned: " + "```" + str(retval) + "```")
    else:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + str(args))
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + str(kwargs))
        if cbkwargs["show_task_return_value"]:
            lines.append("Returned: " + str(retval))

    success = "\n".join(lines)

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": cbkwargs["slack_task_success_color"],
                "text": success,
                "title": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    if cbkwargs["flower_base_url"]:
        attachment["attachments"][0]["title_link"] = (
            cbkwargs["flower_base_url"] +
            "/task/{tid}".format(tid=task_id)
        )

    return attachment

def get_task_duplicate_attachment(task_name, retval, task_id,
                                args, kwargs, **cbkwargs):
    """Create the slack message attachment for a task duplicate state."""
    if (cbkwargs["exclude_tasks"] and
            any([re.search(task, task_name)
                for task in cbkwargs["exclude_tasks"]])):
        STOPWATCH.pop(task_id)
        return
    elif (cbkwargs["include_tasks"] and
            not any([re.search(task, task_name)
                    for task in cbkwargs["include_tasks"]])):
        STOPWATCH.pop(task_id)
        return

    if isinstance(retval, dict):
        retval = json.dumps(retval, indent=4)
    else:
        retval = str(retval)

    message = "DUPLICATE -- " + task_name.rsplit(".", 1)[-1]

    elapsed = divmod(time.time() - STOPWATCH.pop(task_id), 60)

    lines = ["Name: *" + task_name + "*"]

    if cbkwargs["show_task_execution_time"]:
        lines.append("Execution time: {m} minutes {s} seconds".format(
            m=str(int(elapsed[0])),
            s=str(int(elapsed[1])),
        ))
    if cbkwargs["show_task_id"]:
        lines.append("Task ID: " + task_id)

    if cbkwargs["use_fixed_width"]:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + "`" + str(args) + "`")
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + "`" + str(kwargs) + "`")
        if cbkwargs["show_task_return_value"]:
            lines.append("Returned: " + "```" + str(retval) + "```")
    else:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + str(args))
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + str(kwargs))
        if cbkwargs["show_task_return_value"]:
            lines.append("Returned: " + str(retval))

    success = "\n".join(lines)

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": cbkwargs["slack_task_duplicate_color"],
                "text": success,
                "title": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    if cbkwargs["flower_base_url"]:
        attachment["attachments"][0]["title_link"] = (
            cbkwargs["flower_base_url"] +
            "/task/{tid}".format(tid=task_id)
        )

    return attachment


def get_task_failure_attachment(task_name, exc, task_id, args,
                                kwargs, einfo, **cbkwargs):
    """Create the slack message attachment for task failure."""
    if (cbkwargs["exclude_tasks"] and
            any([re.search(task, task_name)
                for task in cbkwargs["exclude_tasks"]])):
        STOPWATCH.pop(task_id)
        return
    elif (cbkwargs["include_tasks"] and
            not any([re.search(task, task_name)
                    for task in cbkwargs["include_tasks"]])):
        STOPWATCH.pop(task_id)
        return

    message = "FAILURE -- " + task_name.rsplit(".", 1)[-1]

    elapsed = divmod(time.time() - STOPWATCH.pop(task_id), 60)

    lines = ["Name: *" + task_name + "*"]

    if cbkwargs["show_task_execution_time"]:
        lines.append("Execution time: {m} minutes {s} seconds".format(
            m=str(int(elapsed[0])),
            s=str(int(elapsed[1])),
        ))
    if cbkwargs["show_task_id"]:
        lines.append("Task ID: " + task_id)

    if cbkwargs["use_fixed_width"]:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + "`" + str(args) + "`")
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + "`" + str(kwargs) + "`")
        lines.append("Exception: " + "`" + str(exc) + "`")
        if cbkwargs["show_task_exception_info"]:
            lines.append("Info: " + "```" + str(einfo) + "```")
    else:
        if cbkwargs["show_task_args"]:
            lines.append("args: " + str(args))
        if cbkwargs["show_task_kwargs"]:
            lines.append("kwargs: " + str(kwargs))
        lines.append("Exception: " + str(exc))
        if cbkwargs["show_task_exception_info"]:
            lines.append("Info: " + str(einfo))

    failure = "\n".join(lines)

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": cbkwargs["slack_task_failure_color"],
                "text": failure,
                "title": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    if cbkwargs["flower_base_url"]:
        attachment["attachments"][0]["title_link"] = (
            cbkwargs["flower_base_url"] +
            "/task/{tid}".format(tid=task_id)
        )

    return attachment


def get_celery_startup_attachment(**kwargs):
    """Create the slack message attachment for celery startup."""
    if kwargs["show_celery_hostname"]:
        message = "*Celery is starting up on {}.*".format(
            socket.gethostname()
        )
    else:
        message = "*Celery is starting up.*"

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": kwargs["slack_celery_startup_color"],
                "text": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    return attachment


def get_celery_shutdown_attachment(**kwargs):
    """Create the slack message attachment for celery shutdown."""
    if kwargs["show_celery_hostname"]:
        message = "_Celery is shutting down on {}._".format(
            socket.gethostname()
        )
    else:
        message = "_Celery is shutting down._"

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": kwargs["slack_celery_shutdown_color"],
                "text": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    return attachment


def get_beat_init_attachment(**kwargs):
    """Create the slack message attachment for beat init."""
    if kwargs["show_celery_hostname"]:
        message = "*Beat is (re)initializing on {}*".format(
            socket.gethostname()
        )
    else:
        message = "*Beat is (re)initializing*"

    beat_schedule = kwargs["beat_schedule"]
    if beat_schedule:
        message += " *with schedule:*"

        sched = []
        for task in sorted(beat_schedule):
            if kwargs["beat_show_full_task_path"]:
                sched.append(
                    task + BEAT_DELIMITER +
                    schedule_to_string(beat_schedule[task]["schedule"]))
            else:
                sched.append(
                    task.split(".", 2)[-1] + BEAT_DELIMITER +
                    schedule_to_string(beat_schedule[task]["schedule"]))
        schedule = (
            "\n*Task{}crontab(m/h/d/dM/MY) OR solar OR interval:*\n".format(
                BEAT_DELIMITER
            ) +
            "```" + "\n".join(sched) + "```"
        )
    else:
        message = message[:-1] + "." + message[-1:]
        schedule = ""

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": kwargs["slack_beat_init_color"],
                "text": message + schedule,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    return attachment


processes = {
    "MainProcess": "Celery",
    "Beat": "Beat"
}


def get_broker_disconnect_attachment(**kwargs):
    """Create the slack message attachment for broker disconnection."""
    if kwargs["show_celery_hostname"]:
        message = "*{process} could not connect to broker on {host}.*".format(
            process=processes.get(
                current_process()._name, current_process()._name),
            host=socket.gethostname()
        )
    else:
        message = "*{process} could not connect to broker.*".format(
            process=processes.get(
                current_process()._name, current_process()._name),
        )

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": kwargs["slack_broker_disconnect_color"],
                "text": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    return attachment


def get_broker_connect_attachment(**kwargs):
    """Create the slack message attachment for broker connection."""
    if kwargs["show_celery_hostname"]:
        message = "*{process} (re)connected to broker on {host}.*".format(
            process=processes.get(
                current_process()._name, current_process()._name),
            host=socket.gethostname()
        )
    else:
        message = "*{process} (re)connected to broker.*".format(
            process=processes.get(
                current_process()._name, current_process()._name),
        )

    attachment = {
        "attachments": [
            {
                "fallback": message,
                "color": kwargs["slack_broker_connect_color"],
                "text": message,
                "mrkdwn_in": ["text"]
            }
        ],
        "text": ""
    }

    return attachment


def schedule_to_string(schedule):
    """Transform a crontab, solar, or timedelta to a string."""
    if isinstance(schedule, crontab):
        return str(schedule)[10:-15]
    elif CELERY_VERSION >= "4.0.0" and isinstance(schedule, solar):
        return str(schedule)[8:-1]
    elif isinstance(schedule, timedelta):
        return "every " + str(schedule)
    else:
        return "every " + str(schedule) + " seconds"
