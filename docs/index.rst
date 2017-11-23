.. celery-slack documentation master file, created by
   sphinx-quickstart on Thu Nov 23 08:00:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

celery-slack
============

Celery-slack is a `Celery <http://docs.celeryproject.org/en/latest/index.html>`_
extension that posts messages to a Slack channel
regarding a Celery application, its beat schedule, and its worker task
execution. Optionally, those messages can link to
`Flower <http://flower.readthedocs.io/en/latest/>`_ task pages.

.. image:: images/celery-slack.png

Prerequisites
-------------

To use this package you will need a Slack App that is part of your
organization's Slack workspace. You can create an App from
`this page <https://api.slack.com/apps>`_. This App should have an incoming
webhook registered to one of your Slack channels. See
`Slack incoming webhooks <https://api.slack.com/incoming-webhooks>`_ for more
information.

Installation
------------

Celery-slack is a python package available on pypi and is compatible with
Python 3. It can be installed using ``pip``:

.. code-block:: python

   pip install celery-slack

Documentation
-------------

.. toctree::
   :maxdepth: 2

   slack
   usage
   notes

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
