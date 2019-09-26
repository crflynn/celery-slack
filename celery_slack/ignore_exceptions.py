def ignore_exceptions(*exceptions):
    """
    :type exceptions: typing.List[Exception]
    """

    def wrapper(f):
        annotations = getattr(f, "__annotations__", {})
        f.__annotations__ = annotations
        f.__annotations__["ignore_exceptions"] = exceptions
        return f

    return wrapper
