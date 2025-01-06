import logging


def verbosity_level_testing_helper():
    """Helper function for testing the verbosity level setting function.

    This function will log messages with different log levels to the modelguard logger.

    """

    logger = logging.getLogger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
