"""Celery state and task callbacks."""
from functools import wraps

from .attachments import get_beat_init_attachment
from .attachments import get_celery_shutdown_attachment
from .attachments import get_celery_startup_attachment
from .attachments import get_task_failure_attachment
from .attachments import get_task_prerun_attachment
from .attachments import get_task_success_attachment
from .attachments import add_task_to_stopwatch
from .slack import post_to_slack


def slack_task_prerun(task_id, task, args, kwargs, **cbkwargs):
    """Initialize the task timer.

    This function connects to the task_prerun signal in order to be able to
    output execution time on tasks.
    """
    add_task_to_stopwatch(task_id)

    if cbkwargs["show_task_prerun"]:

        attachment = get_task_prerun_attachment(
            task_id, task, args, kwargs, **cbkwargs)

        post_to_slack(cbkwargs["webhook"], ' ', attachment)


def slack_task_success(**cbkwargs):
    """Wrap the app.Task.on_success() method with this callback."""
    def wrapper(func):

        @wraps(func)
        def wrapped_func(self, retval, task_id, args, kwargs):
            """Post a message to slack for successful task completion.

            This function is meant to decorate app.Task.on_success where app is
            an instance of a Celery() object, thus it has the same signature.
            """
            attachment = get_task_success_attachment(
                self.name, retval, task_id, args, kwargs, **cbkwargs)

            if attachment:
                post_to_slack(cbkwargs["webhook"], ' ', attachment)

            return func(self, retval, task_id, args, kwargs)

        return wrapped_func

    return wrapper


def slack_task_failure(**cbkwargs):
    """Wrap the app.Task.on_failure() method with this callback."""
    def wrapper(func):

        @wraps(func)
        def wrapped_func(self, exc, task_id, args, kwargs, einfo):
            """Post a message to slack for failed task completion.

            This function is meant to patch app.Task.on_failure where app is an
            instance of a Celery() object, thus it has the same signature.
            """
            attachment = get_task_failure_attachment(
                self.name, exc, task_id, args, kwargs, einfo, **cbkwargs)

            if attachment:
                post_to_slack(cbkwargs["webhook"], ' ', attachment)

            return func(self, exc, task_id, args, kwargs, einfo)

        return wrapped_func

    return wrapper


def slack_celery_startup(**kwargs):
    """Post a message to slack when celery starts.

    This function is connected to the celeryd_init signal.
    """
    attachment = get_celery_startup_attachment(**kwargs)

    post_to_slack(kwargs["webhook"], ' ', attachment)


def slack_celery_shutdown(**kwargs):
    """Post a message to slack when celery starts.

    This function is connected to the worker_shutdown signal.
    """
    attachment = get_celery_shutdown_attachment(**kwargs)

    post_to_slack(kwargs["webhook"], ' ', attachment)


def slack_beat_init(**kwargs):
    """Post a message to slack when celery starts.

    This function is connected to the beat_init signal.
    """
    attachment = get_beat_init_attachment(**kwargs)

    post_to_slack(kwargs["webhook"], ' ', attachment)
