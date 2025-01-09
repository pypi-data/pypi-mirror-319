from typing import Any

from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.middleware import DefineMiddleware
from litestar.plugins import InitPluginProtocol
from litestar.types import Middleware, ExceptionHandlersMap

from pydentity.authentication import AuthenticationError
from pydentity.authorization import AuthorizationError
from pydentity.contrib.litestar.base import LitestarHttpContextAccessor, default_exception_handler, is_async_dependency
from pydentity.contrib.litestar.middleware import AuthenticationMiddleware
from pydentity.exc import InvalidOperationException
from pydentity.identity_builder import IdentityBuilder


class PydentityPlugin(InitPluginProtocol):
    def __init__(
        self,
        builder: IdentityBuilder,
        authentication_exception_handler: "ExceptionHandler | None" = None,
        authorization_exception_handler: "ExceptionHandler | None" = None,
        raise_error: bool = False,
    ) -> None:
        self._raise_error = raise_error
        self._authentication_exception_handler = authentication_exception_handler or default_exception_handler(
            message="Unauthorized", status_code=401
        )
        self._authorization_exception_handler = authorization_exception_handler or default_exception_handler(
            message="Forbidden", status_code=403
        )
        self._dependencies = builder.dependencies
        super().__init__()

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        self._add_dependencies(app_config.dependencies)
        self._try_add_middleware(app_config.middleware)
        self._try_add_exception_handlers(app_config.exception_handlers)
        return app_config

    def _try_add_middleware(self, middlewares: list[Middleware]):
        auth_middleware: DefineMiddleware | None = None
        for middleware in middlewares:
            if isinstance(middleware, DefineMiddleware) and middleware.middleware is AuthenticationMiddleware:
                auth_middleware = middleware

        if not auth_middleware:
            dependency = self._dependencies["schemes"]
            if callable(dependency):
                dependency = dependency()
            middlewares.append(
                DefineMiddleware(AuthenticationMiddleware, schemes=dependency, raise_error=self._raise_error)
            )

    def _try_add_exception_handlers(self, exception_handlers: ExceptionHandlersMap):
        if AuthenticationError not in exception_handlers:
            exception_handlers[AuthenticationError] = self._authentication_exception_handler
        if AuthorizationError not in exception_handlers:
            exception_handlers[AuthorizationError] = self._authorization_exception_handler

    def _add_dependencies(self, dependencies: dict[str, Any]):
        self._dependencies["context_accessor"] = LitestarHttpContextAccessor
        for dependency_key, dependency in self._dependencies.items():
            if dependency_key in dependencies:
                raise InvalidOperationException(f"Duplicate dependency detected: '{dependency_key}'.")
            sync_to_thread = None if is_async_dependency(dependency) else False
            dependencies[dependency_key] = Provide(dependency, sync_to_thread=sync_to_thread)
