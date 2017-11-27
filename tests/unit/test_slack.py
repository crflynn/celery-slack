"""Test slack functions."""
import os
import pytest

import celery_slack
from celery_slack.slack import post_to_slack
from celery_slack.slack import post_warning_to_slack

# local or travis
try:
    from ..secret import slack_webhook
except:
    slack_webhook = os.environ['SLACK_WEBHOOK']



SAMPLE_ATTACHMENT = {
    "attachments": [
        {
            "fallback": "sample message",
            "color": "#36A64F",
            "text": "*sample* _message_",
            "mrkdwn_in": ["text"]
        }
    ],
    "text": ''
}


@pytest.mark.parametrize('test_webhook,slack_attachment,code,cassette', [
    (slack_webhook, SAMPLE_ATTACHMENT, 200, 'real_attach'),
    (slack_webhook, None, 200, 'real_none'),
    ('https://hooks.slack.com/services/X/Y/Z', SAMPLE_ATTACHMENT, 404,
        'fake_attach'),
    ('https://hooks.slack.com/services/X/Y/Z', None, 404, 'fake_none'),
])
def test_post_to_slack(test_webhook, slack_attachment, code, recorder,
                       cassette):
    """Test posting to slack."""
    with recorder.use_cassette('post_to_slack_{code}_{name}'.format(
            code=code,
            name=cassette)):
        response = post_to_slack(test_webhook, ' ', slack_attachment)
    assert response.status_code == code


@pytest.mark.parametrize('slack_attachment,cassette', [
    (SAMPLE_ATTACHMENT, 'attach'),
    (None, 'none'),
])
def test_post_warning_to_slack(webhook, slack_attachment, recorder, cassette):
    """Test posting a rate limit warning to slack."""
    with recorder.use_cassette('post_warning_to_slack_{attach}'.format(
            attach=cassette)):
        response = post_warning_to_slack(webhook, ' ', slack_attachment)
    assert response.status_code == 200


def test_rate_limited(webhook, slack_attachment, mocker):
    """Test rate limited."""
    mocked_time = mocker.patch('celery_slack.slack.time.time')
    mocked_time.return_value = 100
    celery_slack.slack.RETRY_AFTER = 101
    response = post_to_slack('webhook', ' ', slack_attachment)
    assert not response
