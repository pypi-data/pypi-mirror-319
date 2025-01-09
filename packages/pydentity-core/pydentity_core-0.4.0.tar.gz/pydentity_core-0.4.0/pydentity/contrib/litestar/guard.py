from collections.abc import Iterable
from typing import Callable, Awaitable

from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler

from pydentity.authorization import Authorize

__all__ = ("authorize",)


def authorize(
    roles: Iterable[str] | str | None = None, policy: str | None = None
) -> Callable[[ASGIConnection, BaseRouteHandler], Awaitable[None]]:
    """
    Indicates that the route or router to which this dependency is applied requires the specified authorization.

    :param roles: A list of roles that are allowed to access the resource.
    :param policy: Policy name that determines access to the resource.
    :return:
    :raise InvalidOperationException: If the specified policy name is not found.
    :raise AuthorizationError: If authorization failed.
    """

    async def call_authorize(connection: ASGIConnection, _: BaseRouteHandler) -> None:
        await Authorize(roles, policy)(connection)

    return call_authorize
