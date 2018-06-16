Release History
---------------

0.3.0 (2018-06-16)
~~~~~~~~~~~~~~~~~~

* Add messages for celery/beat disconnection/reconnection to broker
* Add option to override the Slack request timeout value

0.2.0 (2018-06-10)
~~~~~~~~~~~~~~~~~~

* Add options to disable celery startup/shutdown messages
* Add option to disable beat messages

0.1.4 (2018-01-17)
~~~~~~~~~~~~~~~~~~

* Change default behavior of task prerun messages to false
* Add sorted tasks for beat init message with beat schedule
* Add 1 second timeout to Slack post requests
* Use the responses library to mock requests in 2.7 and 3.3 tests

0.1.3 (2017-11-28)
~~~~~~~~~~~~~~~~~~

* Fix socket error by replacing session object with requests functional api
* Replace betamax test fixture with vcrpy recorder

0.1.2 (2017-11-27)
~~~~~~~~~~~~~~~~~~

* Compatibility fix for Python 2.7

0.1.1 (2017-11-27)
~~~~~~~~~~~~~~~~~~

* Setup travis-ci, codecov
* Compatibility fix for solar schedules and Celery 4.0

0.1.0 (2017-11-27)
~~~~~~~~~~~~~~~~~~

* First release.
* Slack notifications for beat init, celery startup/shutdown, task prerun/success/failure.
* Several options related to presentation, task filtration, and attachment colors.
