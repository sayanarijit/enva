__version__ = "0.1.0"


from os import environ


def define(var="ENVIRONMENT", **kwargs):
    """Define your environments.

    Arguments:
        var: Name of the environment variable to differentiate between environments.
        **kwargs: keys mapping to the names of the different environments.
    """

    env = environ.get(var)
    keys = {val: key for key, val in kwargs.items()}
    key = keys.get(env)

    def env(default=None, **kwargs):
        """Get the value based on the current environment.

        Arguments:
            default: default value to return if no key matches the current environment.
            **kwargs: keys mapping to the values for different environments.

        Exceptions:
            KeyError: When default if not
        """
        val = kwargs.get(key, default)

        if val is None and default is None:
            raise KeyError("default")

        return default if val is None else val

    return env
