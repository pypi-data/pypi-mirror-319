from collections.abc import Iterable
from typing import Any

from fastapi import Depends
from starlette.requests import Request

from pydentity.authorization import Authorize

__all__ = ("authorize",)


def authorize(roles: Iterable[str] | str | None = None, policy: str | None = None) -> Any:
    """
    Indicates that the route or router to which this dependency is applied requires the specified authorization.

    :param roles: A list of roles that are allowed to access the resource.
    :param policy: Policy name that determines access to the resource.
    :return:
    :raise InvalidOperationException: If the specified policy name is not found.
    :raise AuthorizationError: If authorization failed.
    """

    async def call_authorize(request: Request) -> None:
        await Authorize(roles, policy)(request)

    return Depends(call_authorize)
