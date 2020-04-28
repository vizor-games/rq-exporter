"""
RQ exporter module.

Register the RQ collector and create the WSGI application instance.

"""

import logging

from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY

from .collector import RQCollector
from .utils import get_redis_connection
from . import config


logger = logging.getLogger(__name__)


def register_collector():
    """Register the RQ collector instance.

    Raises:
        IOError: From `get_redis_connection` if there was an error opening
            the password file.
        redis.exceptions.RedisError: On Redis connection errors.

    """
    # Register the RQ collector
    # The `collect` method is called on registration
    REGISTRY.register(RQCollector(
        get_redis_connection()
    ))


def create_app():
    """Create a WSGI application.

    Register the `RQCollector` instance and then return a WSGI application.
    This function is suitable for use by WSGI servers like Gunicorn to load
    the WSGI application.

    Example:
        gunicorn "rq_exporter:create_app()"

    Returns:
        function: WSGI application function.

    """
    logging.basicConfig(
        format = config.LOG_FORMAT,
        datefmt = config.LOG_DATEFMT,
        level = config.LOG_LEVEL
    )

    logger.debug('Registering the RQ collector...')

    register_collector()

    logger.debug('RQ collector registered')

    return make_wsgi_app()
