from litestar import Request
from litestar.enums import ScopeType
from litestar.middleware import AbstractMiddleware
from litestar.types import ASGIApp, Scope, Receive, Send

from pydentity.authentication import AuthenticationError, AuthenticationSchemeProvider
from pydentity.authentication.interfaces import IAuthenticationSchemeProvider
from pydentity.exc import InvalidOperationException
from pydentity.http.context import HttpContext

__all__ = ("AuthenticationMiddleware",)


class AuthenticationMiddleware(AbstractMiddleware):
    scopes = {ScopeType.HTTP, ScopeType.WEBSOCKET}
    exclude_opt_key = "allowanonymous"

    def __init__(
        self,
        app: ASGIApp,
        schemes: IAuthenticationSchemeProvider,
        raise_error: bool = False,
    ) -> None:
        super().__init__(app)
        self.schemes = schemes
        self.raise_error = raise_error

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["user"] = None
        scope["auth"] = False

        context = HttpContext(Request(scope), None, self.schemes)
        default_authenticate = self.schemes.get_default_authentication_scheme()

        if default_authenticate is None:
            raise InvalidOperationException("Scheme not found.")

        if result := await context.authenticate(default_authenticate.name):
            scope["user"] = result.principal
            scope["auth"] = result.principal.identity.is_authenticated
        elif self.raise_error:
            raise AuthenticationError()

        await self.app(scope, receive, send)
