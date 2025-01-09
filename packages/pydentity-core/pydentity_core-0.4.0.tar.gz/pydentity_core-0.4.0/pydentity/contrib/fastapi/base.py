from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from starlette.types import ExceptionHandler

from pydentity.authentication.interfaces import IAuthenticationSchemeProvider
from pydentity.http.context import HttpContextAccessor


def default_exception_handler(message: str, status_code: int) -> ExceptionHandler:
    def exception_handler(request: Request, exc: Exception) -> Response:
        return PlainTextResponse(message, status_code=status_code)

    return exception_handler


class FastapiHttpContextAccessor(HttpContextAccessor):
    response_class = Response

    def __init__(self, request: Request, schemes: IAuthenticationSchemeProvider):
        super().__init__(request, schemes)
