__version__ = "0.1.1"


from os import environ as _environ


def define(var="ENVIRONMENT", *args, **kwargs):
    """Define your environments.

    Arguments:
        var: Name of the environment variable to differentiate between environments.
        **kwargs: keys mapping to the names of the different environments.
    """

    for arg in args:
        if arg not in kwargs:
            kwargs[arg] = arg

    env = _environ.get(var)
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

        if isinstance(val, FromEnv):
            val = val.val()

        return default if val is None else val

    return env


class FromEnv:
    def __init__(self, var, type=str):
        self.var = var
        self.type = type

    def val(self):
        return self.type(_environ[self.var])


def environ(var, type=str):
    """Parse value from environment variable if the environment matches."""

    return FromEnv(var, type=type)
