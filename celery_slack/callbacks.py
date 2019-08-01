"""Celery state and task callbacks."""
from functools import wraps
import time

from .attachments import get_beat_init_attachment
from .attachments import get_broker_connect_attachment
from .attachments import get_broker_disconnect_attachment
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

        # if task already in stopwatch, skip pre-run callback should be a no-op
        # this prevents retry-looping tasks from updating the stopwatch on each retry attempt

        initial_run = add_task_to_stopwatch(task_id)

        if cbkwargs["show_task_prerun"] and initial_run:

            attachment = get_task_prerun_attachment(
                task_id, task, args, kwargs, **cbkwargs)

            post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

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

            # if not self.request.is_eager and self.AsyncResult(task_id).status == 'DUPLICATE':
            #     attachment = get_task_duplicate_attachment(
            #         self.name, retval, task_id, args, kwargs, **cbkwargs
            #     )
            # else:

            attachment = get_task_success_attachment(
                self.name, retval, task_id, args, kwargs, **cbkwargs)

            if attachment:
                post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["success_emoji"],
                "channel": cbkwargs["channel"],
            })

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
                post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["failure_emoji"],
                "channel": cbkwargs["channel"],
            })

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

        post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

    return slack_celery_startup_callback


def slack_celery_shutdown(**cbkwargs):
    """Return the celery_shutdown callback."""
    def slack_celery_shutdown_callback(**kwargs):
        """Post a message to slack when celery starts.

        This function is connected to the worker_shutdown signal.
        """
        attachment = get_celery_shutdown_attachment(**cbkwargs)

        post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

    return slack_celery_shutdown_callback


def slack_beat_init(**cbkwargs):
    """Return the beat_init callback."""
    def slack_beat_init_callback(**kwargs):
        """Post a message to slack when celery starts.

        This function is connected to the beat_init signal.
        """
        attachment = get_beat_init_attachment(**cbkwargs)

        post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

    return slack_beat_init_callback


# Prevent spam
BROKER_COOLDOWN = 60
# Assume connected at start
BROKER_CONNECTED = True
BROKER_DISCONNECT_TIME = time.time() - BROKER_COOLDOWN
BROKER_CONNECT_TIME = time.time() - BROKER_COOLDOWN


def slack_broker_disconnect(**cbkwargs):
    """Wrap the kombu.connection.retry_over_time callback callable."""
    def slack_broker_disconnect_callback():
        """Post to slack and reset the cooldown on connect."""
        global BROKER_DISCONNECT_TIME
        global BROKER_CONNECT_TIME
        global BROKER_COOLDOWN
        global BROKER_CONNECTED

        BROKER_CONNECT_TIME = time.time() - BROKER_COOLDOWN

        if time.time() - BROKER_DISCONNECT_TIME > BROKER_COOLDOWN:
            BROKER_CONNECTED = False
            BROKER_DISCONNECT_TIME = time.time()
            attachment = get_broker_disconnect_attachment(**cbkwargs)
            post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

    def wrapper(func):

        @wraps(func)
        def wrapped_func(fun, catch, args=[], kwargs={}, errback=None,
                    max_retries=None, interval_start=2, interval_step=2,
                    interval_max=30, callback=None):

            def callback_wrapper(cb_func):
                @wraps(cb_func)
                def wrapped_cb_func(*args, **kwargs):
                    slack_broker_disconnect_callback()
                    return cb_func(*args, **kwargs)
                return wrapped_cb_func

            if callback is not None:
                callback = callback_wrapper(callback)
            else:
                callback = slack_broker_disconnect_callback

            func(fun=fun, catch=catch, args=args, kwargs=kwargs,
                errback=errback, max_retries=max_retries,
                interval_start=interval_start, interval_step=interval_step,
                interval_max=interval_max, callback=callback)

        return wrapped_func

    return wrapper


def slack_broker_connect(**cbkwargs):
    """Wrap the kombu.connection.retry_over_time function."""
    def slack_broker_connect_callback():
        """Post to slack and reset the cooldown on disconnect."""
        global BROKER_DISCONNECT_TIME
        global BROKER_CONNECT_TIME
        global BROKER_COOLDOWN
        global BROKER_CONNECTED

        BROKER_DISCONNECT_TIME = time.time() - BROKER_COOLDOWN
        passed_cooldown = time.time() - BROKER_CONNECT_TIME > BROKER_COOLDOWN

        if not BROKER_CONNECTED and passed_cooldown:
            BROKER_CONNECTED = True
            BROKER_CONNECT_TIME = time.time()
            attachment = get_broker_connect_attachment(**cbkwargs)
            post_to_slack(cbkwargs["webhook"], " ", attachment, payload={
                "username": cbkwargs["username"],
                "icon_emoji": cbkwargs["default_emoji"],
                "channel": cbkwargs["channel"],
            })

    def wrapper(func):

        @wraps(func)
        def wrapped_func(fun, catch, args=[], kwargs={}, errback=None,
                    max_retries=None, interval_start=2, interval_step=2,
                    interval_max=30, callback=None):

            try:
                func(fun=fun, catch=catch, args=args, kwargs=kwargs,
                        errback=errback, max_retries=max_retries,
                        interval_start=interval_start,
                        interval_step=interval_step,
                        interval_max=interval_max, callback=callback)
            except Exception as exc:  # pragma: no cover
                raise exc

            slack_broker_connect_callback()

        return wrapped_func

    return wrapper
