"""The celery beat schedule."""
import datetime
import pytz

from celery import __version__ as CELERY_VERSION
from celery.schedules import crontab

if CELERY_VERSION >= "4.0.0":
    from celery.schedules import solar


TZ = pytz.timezone("UTC")

# Launch one time on restart

one_timers = {
    "tests.celeryapp.tasks.successful_task": {"args": [1, 2], "kwargs": {}},
    "tests.celeryapp.tasks.unsuccessful_task": {"args": [1, 2], "kwargs": {}},
}

solar_tasks = {"tests.celeryapp.tasks.solar_task": {"args": [1, 2], "kwargs": {}}}
timedelta_tasks = {"tests.celeryapp.tasks.timedelta_task": {"args": [1, 2], "kwargs": {}}}
number_tasks = {"tests.celeryapp.tasks.number_task": {"args": [1, 2], "kwargs": {}}}


# The beat schedule
schedule = {}


def add_tasks_to_schedule(tasks, ctab):
    """Add the tasks to the schedule."""
    for task in tasks:
        name = task

        the_task = {
            name: {"task": task, "args": tasks[task]["args"], "kwargs": tasks[task]["kwargs"], "schedule": ctab}
        }
        schedule.update(the_task)


def get_schedule():
    """Create the celerybeat schedule."""
    # one time for testing
    now = datetime.datetime.now(TZ)
    add_tasks_to_schedule(
        one_timers,
        crontab(
            hour=(now.hour + (1 if now.minute + 1 == 60 else 0)) % 24,
            minute=(now.minute + 1) % 60,
            day_of_month=now.day,
            month_of_year=now.month,
        ),
    )
    if CELERY_VERSION >= "4.0.0":
        add_tasks_to_schedule(solar_tasks, solar("sunset", 50, 50))
    add_tasks_to_schedule(timedelta_tasks, datetime.timedelta(5))
    add_tasks_to_schedule(number_tasks, 1000)
    return schedule


def get_imports(sched=None):
    """Get all the modules for a celery worker to import."""
    sched = sched or schedule
    modules_to_import = [task["task"].rsplit(".", 1)[0] for task in sched.values()]
    return list(set(modules_to_import))
