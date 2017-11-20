"""Common test functions."""
import copy


def get_options(default, **kwargs):
    """Get full options dict."""
    options = copy.deepcopy(default)
    options.update(**kwargs)
    return options
