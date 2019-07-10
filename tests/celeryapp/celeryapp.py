"""The celery app."""
import logging
import os

from celery import Celery

from celery_slack import Slackify
from .schedule import get_schedule

try:
    from ..secret import slack_webhook
except Exception:
    slack_webhook = os.environ["SLACK_WEBHOOK"]


logging.basicConfig(level="INFO")


schedule = get_schedule()

app = Celery("schedule")
app.config_from_object("tests.celeryapp.config")

options = {
    "flower_base_url": "https://flower.example.com",
    "webhook": slack_webhook,
    "beat_schedule": schedule,
    "show_beat": True,
    # "show_task_prerun": True,
    # "failures_only": True,
    # "show_celery_hostname": True,
    # "show_startup": False,
    # "show_shutdown": False,
    "slack_request_timeout": 3,
    "show_broker": True,
}

# logging.info("Creating celery-slack object.")
slack_app = Slackify(app, **options)
# slack_app = Slackify(app, slack_webhook)
# logging.info("Created celery-slack object.")


if __name__ == "__main__":
    app.start()
