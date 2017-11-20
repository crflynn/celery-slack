"""Celery-slack exceptions."""
# flake8: noqa D103


class CelerySlackException(Exception):
    pass


class MissingWebhookException(CelerySlackException):
    pass


class TaskFiltrationException(CelerySlackException):
    pass


class InvalidColorException(CelerySlackException):
    pass
