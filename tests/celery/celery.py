"""The celery app."""
from celery import Celery

# from celery_slack import Slackify
from .schedule import get_schedule
# from ..secret import slack_webhook


schedule = get_schedule()

app = Celery('schedule')
app.config_from_object('test.celery.config')

# options = {
#     "flower_base_url": "https://flower.example.com",
#     "webhook": slack_webhook,
#     "schedule": schedule,
#     "show_task_prerun": True,
#     "failures_only": True,
# }
# slack_app = Slackify(app, **options)


if __name__ == '__main__':
    app.start()
