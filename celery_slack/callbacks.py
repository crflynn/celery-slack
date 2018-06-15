"""Celery state and task callbacks."""
from functools import wraps
import time

from .attachments import get_beat_init_attachment
from .attachments import get_broker_disconnection_attachment
from .attachments import get_celery_shutdown_attachment
from .attachments import get_celery_startup_attachment
from .attachments import get_task_failure_attachment
from .attachments import get_task_prerun_attachment
from .attachments import get_task_success_attachment
from .attachments import add_task_to_stopwatch
from .slack import post_to_slack


def slack_task_prerun(**cbkwargs):
    """Return the task_prerun callback."""
    def slack_task_prerun_callback(task_id, task, args, kwargs, **skwargs):
        """Initialize the task timer.

        This function connects to the task_prerun signal in order to be able to
        output execution time on tasks.
        """
        add_task_to_stopwatch(task_id)

        if cbkwargs["show_task_prerun"]:

            attachment = get_task_prerun_attachment(
                task_id, task, args, kwargs, **cbkwargs)

            post_to_slack(cbkwargs["webhook"], ' ', attachment)

    return slack_task_prerun_callback


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


def slack_celery_startup(**cbkwargs):
    """Return the celery_startup callback."""
    def slack_celery_startup_callback(**kwargs):
        """Post a message to slack when celery starts.

        This function is connected to the celeryd_init signal.
        """
        attachment = get_celery_startup_attachment(**cbkwargs)

        post_to_slack(cbkwargs["webhook"], ' ', attachment)

    return slack_celery_startup_callback


def slack_celery_shutdown(**cbkwargs):
    """Return the celery_shutdown callback."""
    def slack_celery_shutdown_callback(**kwargs):
        """Post a message to slack when celery starts.

        This function is connected to the worker_shutdown signal.
        """
        attachment = get_celery_shutdown_attachment(**cbkwargs)

        post_to_slack(cbkwargs["webhook"], ' ', attachment)

    return slack_celery_shutdown_callback


def slack_beat_init(**cbkwargs):
    """Return the beat_init callback."""
    def slack_beat_init_callback(**kwargs):
        """Post a message to slack when celery starts.

        This function is connected to the beat_init signal.
        """
        attachment = get_beat_init_attachment(**cbkwargs)

        post_to_slack(cbkwargs["webhook"], ' ', attachment)

    return slack_beat_init_callback


# Prevent spam
BROKER_FAILURE_COOLDOWN = 60
BROKER_FAILURE_TIME = time.time() - BROKER_FAILURE_COOLDOWN


def slack_broker_connection_failure(**cbkwargs):
    """Wrap the kombu.connection.retry_over_time callback callable."""
    def slack_callback():
        global BROKER_FAILURE_TIME
        global BROKER_FAILURE_COOLDOWN

        if time.time() - BROKER_FAILURE_TIME > BROKER_FAILURE_COOLDOWN:
            BROKER_FAILURE_TIME = time.time()
            attachment = get_broker_disconnection_attachment(**cbkwargs)
            post_to_slack(cbkwargs["webhook"], ' ', attachment)

    def wrapper(func):

        @wraps(func)
        def wrapped_func(fun, catch, args=[], kwargs={}, errback=None,
                    max_retries=None, interval_start=2, interval_step=2,
                    interval_max=30, callback=None):

            def callback_wrapper(cb_func):
                @wraps(cb_func)
                def wrapped_cb_func(*args, **kwargs):
                    slack_callback()
                    return cb_func(*args, **kwargs)
                return wrapped_cb_func

            if callback is not None:
                callback = callback_wrapper(callback)
            else:
                callback = slack_callback

            func(fun=fun, catch=catch, args=args, kwargs=kwargs,
                    errback=errback, max_retries=max_retries,
                    interval_start=interval_start, interval_step=interval_step,
                    interval_max=interval_max, callback=callback)

        return wrapped_func

    return wrapper
