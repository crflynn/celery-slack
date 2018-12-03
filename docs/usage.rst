Usage
=====

Basic usage
-----------

The most basic implementation of celery-slack requires a Celery instance object
and a Slack webhook corresponding to a Slack channel. A simple example might
look something like this:

.. code-block:: python

   from celery import Celery
   from celery_slack import Slackify


   # You should NOT commit the actual webhook to your repository.
   SLACK_WEBHOOK = 'https://hooks.slack.com/services/XXX/YYY/ZZZ'

   app = Celery('project')
   app.config_from_object('project.config')

   slack_app = Slackify(app, SLACK_WEBHOOK)


   if __name__ == '__main__':
       app.start()


Advanced usage
--------------

Celery-slack offers a number of configuration options to customize the look
and output of Slack messages. The following are the default options of the
extension:

.. code-block:: javascript

   DEFAULT_OPTIONS = {
       "slack_beat_init_color": "#FFCC2B",
       "slack_broker_connect_color": "#36A64F",
       "slack_broker_disconnect_color": "#D00001",
       "slack_celery_startup_color": "#FFCC2B",
       "slack_celery_shutdown_color": "#660033",
       "slack_task_prerun_color": "#D3D3D3",
       "slack_task_success_color": "#36A64F",
       "slack_task_failure_color": "#D00001",
       "slack_request_timeout": 1,
       "flower_base_url": None,
       "show_celery_hostname": False,
       "show_task_id": True,
       "show_task_execution_time": True,
       "show_task_args": True,
       "show_task_kwargs": True,
       "show_task_exception_info": True,
       "show_task_return_value": True,
       "show_task_prerun": False,
       "show_startup": True,
       "show_shutdown": True,
       "show_beat": True,
       "show_broker": False,
       "use_fixed_width": True,
       "include_tasks": None,
       "exclude_tasks": None,
       "failures_only": False,
       "webhook": None,
       "beat_schedule": None,
       "beat_show_full_task_path": False,
   }


Any subset of these options can be passed to the constructor in the form
of keyword arguments. e.g.

.. code-block:: python

   options = {
       # Some subset of options
   }
   app = Celery('project')
   slack_app = Slackify(app, SLACK_WEBHOOK, **options)


Most of the options are self explanatory, but here are some additional details:

* **slack_\*_color**: The left vertical bar color associated with the slack
  message attachments
* **slack_request_timeout**: The Slack message request timeout in seconds
* **flower_base_url**: e.g. https://flower.example.com, if provided, the slack
  message titles will link to task pages
  in `Flower <http://flower.readthedocs.io/en/latest/>`_
* **show_task_id**: Show the uuid for the task.
* **show_task_execution_time**: Show time to complete task in minutes/seconds
* **show_celery_hostname**: Show the machine hostname on celery/beat messages
* **show_task_args**: Show the task's args
* **show_task_kwargs**: Show the task's keyword args
* **show_task_exception_info**: Show the traceback for failed tasks
* **show_task_return_value**: Show the return value of a successful task
* **show_task_prerun**: Post messages at start of task execution
* **show_startup**: Post message when celery starts
* **show_shutdown**: Post message when celery stops
* **show_beat**: Post message when beat starts
* **show_broker**: Post messages when celery/beat disconnect from or reconnect
    to the broker
* **use_fixed_width**: Use slack fixed width formatting for args, kwargs,
  retval, and exception info
* **include_tasks**: A list of task paths to include. If used, post task
  messages only for these tasks. Uses regex pattern matching.
  e.g. ``module.submodule.taskname`` for a specific task or
  just ``module.submodule`` for all tasks in that submodule. Cannot be used
  in conjunction with ``exclude_tasks``.
* **exclude_tasks**: A list of task paths to exclude. If used, suppress task
  messages only for these tasks. All other tasks will generate slack
  messages. Cannot be used in conjunction with ``include_tasks``. Uses
  regex pattern matching.
* **failures_only**: Only post messages on task failures.
* **webhook**: The only required parameter. A slack webhook corresponding to a
  slack channel.
* **beat_schedule**: The celery beat schedule. If provided, the beat_init
  message will display the schedule. compatible with ``crontab``, ``solar``,
  and ``timedelta`` schedule times.
* **beat_show_full_task_path**: Show the full module-task path. If False
  (default) only show `submodule.taskname`.
