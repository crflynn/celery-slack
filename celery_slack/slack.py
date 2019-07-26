"""Post to slack."""
import logging
import time

import requests
from requests.exceptions import RequestException


RETRY_AFTER = 0
RATE_LIMITED = False
TIMEOUT = 1


def post_to_slack(webhook, text=" ", attachment=None, payload={}):
    """Post a message to the slack channel."""
    global RETRY_AFTER
    global RATE_LIMITED

    if time.time() <= RETRY_AFTER:
        logging.error("Slack: HTTP 429 Too Many Requests.")
        return False
    else:
        if RATE_LIMITED:
            RATE_LIMITED = False
            return post_warning_to_slack(webhook, text, attachment)

    payload.update({"text": text if text != "" else " "})

    if attachment is not None:
        payload.update(attachment)
    try:
        response = None
        response = requests.post(webhook, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
    except RequestException as exc:
        logging.error("Unable to post to Slack; {e}: {msg}".format(
            e=type(exc).__name__, msg=str(exc)))
        if response:
            RETRY_AFTER = \
                time.time() + int(response.headers.get("Retry-After", 0))
            RATE_LIMITED = True

    return response


def post_warning_to_slack(webhook, text, attachment=None):
    """Post a warning to Slack about being rate limited."""
    message = (
        "*WARNING: HTTP 429 Too Many Requests from celery-slack.*\n\n"
        "*You should make adjustments to your schedule and/or restrict "
        "the set of tasks associated with celery-slack before the application "
        "becomes permanently rate-limited or disabled.*"
    )
    warning = {
        "fallback": message,
        "color": "#000000",
        "text": message,
        "mrkdwn_in": ["text"]
    }
    if attachment is None:
        attachment = {
            "attachments": [
                warning
            ],
            "text": ""
        }
    else:
        attachment["attachments"].append(warning)

    payload = {"text": ""}
    payload.update(attachment)
    try:
        response = None
        response = requests.post(webhook, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
    except RequestException as exc:
        logging.error("Unable to post to Slack; {e}: {msg}".format(
            e=type(exc).__name__, msg=str(exc)))

    return response
