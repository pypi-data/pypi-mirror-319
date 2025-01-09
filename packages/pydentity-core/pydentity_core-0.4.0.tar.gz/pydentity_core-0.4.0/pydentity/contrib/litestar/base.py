import inspect

from litestar import Response, Request, MediaType
from litestar.types import ExceptionHandler

from pydentity.authentication.interfaces import IAuthenticationSchemeProvider
from pydentity.http.context import HttpContextAccessor


def is_async_dependency(value):
    def is_async_callable(_o):
        return inspect.iscoroutinefunction(_o) or inspect.isasyncgenfunction(_o)

    return is_async_callable(value) or (callable(value) and is_async_callable(value.__call__))  # type:ignore


def default_exception_handler(message: str, status_code: int) -> ExceptionHandler:
    def exception_handler(request: Request, exc: Exception) -> Response:
        return Response(message, status_code=status_code, media_type=MediaType.TEXT)

    return exception_handler


class LitestarHttpContextAccessor(HttpContextAccessor):
    response_class = Response

    def __init__(self, request: Request, schemes: IAuthenticationSchemeProvider):
        super().__init__(request, schemes)
