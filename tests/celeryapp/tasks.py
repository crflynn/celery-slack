"""Test tasks."""
from tests.celeryapp.celeryapp import app


@app.task
def successful_task(x, y):
    """Add x and y."""
    return {"sample": "json"}


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
