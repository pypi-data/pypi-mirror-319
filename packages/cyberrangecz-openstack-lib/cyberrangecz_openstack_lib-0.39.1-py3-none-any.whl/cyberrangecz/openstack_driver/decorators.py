from typing import Callable, Any

from keystoneauth1 import exceptions as keystone_exception
from cyberrangecz.cloud_commons import exceptions


def check_authentication(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for testing of OpenStackClient authentication and correct settings"""

    def call(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except keystone_exception.ClientException as ex:
            raise exceptions.KypoException(
                "Error while running KypoOstackClient function: {}\n"
                "Either your are not authenticated or your configuration is wrong."
                .format(ex)) from ex

    return call
