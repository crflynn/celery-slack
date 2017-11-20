"""Test tasks."""
# flake8: noqa E501
from .celery import app


@app.task
def successful_task(x, y):
    """Add x and y."""
    return {
       "ResponseMetadata": {
           "RequestId": "c7b0f23b-cc58-11e7-87be-d766f4da3234",
           "RetryAttempts": 0,
           "HTTPStatusCode": 200,
           "HTTPHeaders": {
               "x-amzn-requestid": "c7b0f23b-cc58-11e7-87be-d766f4da3234",
               "date": "Sat, 18 Nov 2017 12:05:34 GMT",
               "content-type": "text/xml",
               "content-length": "338"
           }
       },
       "MessageId": "0100015fcf050827-3df4b4e5-f365-4658-9746-42115b95a08f-000000"
    }


@app.task
def unsuccessful_task(x, y):
    """Raise an exception."""
    raise Exception("Something went wrong.")


@app.task
def solar_task(x, y):
    """Do nothing."""
    return "Solar task."

@app.task
def timedelta_task(x, y):
    """Do nothing."""
    return "Timedelta task."

@app.task
def number_task(x, y):
    """Do nothing."""
    return "Number task."
