"""The celery app."""
import logging
# import sys

from celery import Celery

# from celery_slack import Slackify
from .schedule import get_schedule
# from ..secret import slack_webhook


logging.basicConfig(level='INFO')


schedule = get_schedule()

app = Celery('schedule')
app.config_from_object('tests.celery.config')

# options = {
#     "flower_base_url": "https://flower.example.com",
#     "webhook": slack_webhook,
#     "schedule": schedule,
#     "show_task_prerun": True,
#     "failures_only": True,
# }
#
# logging.info('Creating celery-slack object.')
# slack_app = Slackify(app, **options)
# logging.info('Created celery-slack object.')
#

if __name__ == '__main__':
    app.start()
