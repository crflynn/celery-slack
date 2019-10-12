"""Celery-slack exceptions."""


class CelerySlackException(Exception):
    pass


class MissingWebhookException(CelerySlackException):
    pass


class TaskFiltrationException(CelerySlackException):
    pass


class InvalidColorException(CelerySlackException):
    pass
