class ConfigError(Exception):
    """
    Base exception class for all configuration-related errors.
    """


class InvalidCast(ConfigError):
    """
    Exception raised when the configuration cast callable raises an error.

    This exception is raised when the casting function provided to the configuration
    is unable to successfully cast a value.
    """


class MissingName(ConfigError, KeyError):
    """
    Exception raised when a configuration name is not found in the given environment.

    This exception is raised when attempting to retrieve a configuration value by name,
    but the name is not found in the configuration environment.
    """


class AlreadySet(ConfigError):
    """
    Exception raised when attempting to set a value that is already set.

    This exception is raised when trying to set a value for a configuration that
    has already been set previously.
    """


class StrictCast(InvalidCast):
    """
    Exception raised when a strict cast is used for casting a configuration value.

    This exception is raised when a strict cast is used for casting a value, and
    the cast operation encounters an error.
    """


class InvalidEnv(ConfigError):
    """
    Exception raised when an environment variable does not pass the rule check.

    This exception is raised when an environment variable does not meet the requirements
    specified by the rule check.
    """
