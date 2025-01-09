from collections.abc import AsyncGenerator, AsyncIterator, Coroutine, Generator, Iterable
from typing import Callable, TypeVar, Union, Self

from pydentity.authentication import AuthenticationSchemeProvider, add_authentication
from pydentity.hashers.password_hashers import Argon2PasswordHasher
from pydentity.identity_error_describer import IdentityErrorDescriber
from pydentity.identity_options import IdentityOptions
from pydentity.interfaces.lookup_normalizer import ILookupNormalizer
from pydentity.interfaces.password_hasher import IPasswordHasher
from pydentity.interfaces.password_validator import IPasswordValidator
from pydentity.interfaces.role_validator import IRoleValidator
from pydentity.interfaces.stores import IUserStore, IRoleStore
from pydentity.interfaces.token_provider import IUserTwoFactorTokenProvider
from pydentity.interfaces.user_claims_principal_factory import IUserClaimsPrincipalFactory
from pydentity.interfaces.user_confirmation import IUserConfirmation
from pydentity.interfaces.user_validator import IUserValidator
from pydentity.lookup_normalizer import UpperLookupNormalizer
from pydentity.role_manager import RoleManager
from pydentity.signin_manager import SignInManager
from pydentity.token_providers import (
    DataProtectorTokenProvider,
    PhoneNumberTokenProvider,
    EmailTokenProvider,
    AuthenticatorTokenProvider,
)
from pydentity.types import TUser, TRole
from pydentity.user_claims_principal_factory import UserClaimsPrincipalFactory
from pydentity.user_confirmation import DefaultUserConfirmation
from pydentity.user_manager import UserManager
from pydentity.validators import UserValidator, RoleValidator, PasswordValidator

RETURN_TYPE = TypeVar("RETURN_TYPE")

DependencyCallable = Callable[
    ...,
    Union[
        RETURN_TYPE,
        Coroutine[None, None, RETURN_TYPE],
        AsyncGenerator[RETURN_TYPE, None],
        Generator[RETURN_TYPE, None, None],
        AsyncIterator[RETURN_TYPE],
    ],
]


class _ValidatorWrapper:
    def __init__(self):
        self.items = []

    def __call__(self, error_describer: IdentityErrorDescriber):
        if not self.items:
            return None
        return tuple(item(error_describer) for item in self.items)


class IdentityBuilder:
    def __init__(self, user_store, role_store, configure_options: Callable[[IdentityOptions], None] | None = None):
        options = IdentityOptions()
        if configure_options and callable(configure_options):
            configure_options(options)
        self._dependencies = {
            "schemes": lambda: AuthenticationSchemeProvider(),
            "options": lambda: options,
            "error_describer": lambda: None,
            "user_store": user_store,
            "role_store": role_store,
            "user_validators": _ValidatorWrapper(),
            "role_validators": _ValidatorWrapper(),
            "password_validators": _ValidatorWrapper(),
            "key_normalizer": lambda: None,
            "password_hasher": lambda: None,
            "user_claims_factory": lambda: None,
            "confirmation": lambda: None,
            "user_manager": lambda: None,
            "role_manager": lambda: None,
            "signin_manager": lambda: None,
        }

    @property
    def dependencies(self):
        return self._dependencies.copy()

    def add_user_manager(self, user_manager: DependencyCallable[UserManager[TUser]]) -> Self:
        self._dependencies["user_manager"] = user_manager
        return self

    def add_role_manager(self, role_manager: DependencyCallable[RoleManager[TRole]]) -> Self:
        self._dependencies["role_manager"] = role_manager
        return self

    def add_signin_manager(self, signin_manager: DependencyCallable[SignInManager[TUser]]) -> Self:
        self._dependencies["signin_manager"] = signin_manager
        return self

    def add_lookup_normalizer(self, lookup_normalizer: DependencyCallable[ILookupNormalizer]) -> Self:
        self._dependencies["key_normalizer"] = lookup_normalizer
        return self

    def add_password_hasher(self, password_hasher: DependencyCallable[IPasswordHasher[TUser]]) -> Self:
        self._dependencies["password_hasher"] = password_hasher
        return self

    def add_user_claims_factory(
        self, user_claims_factory: DependencyCallable[IUserClaimsPrincipalFactory[TUser]]
    ) -> Self:
        self._dependencies["user_claims_factory"] = user_claims_factory
        return self

    def add_confirmation(self, confirmation: DependencyCallable[IUserConfirmation[TUser]]) -> Self:
        self._dependencies["confirmation"] = confirmation
        return self

    def add_error_describer(self, error_describer: DependencyCallable[IdentityErrorDescriber]) -> Self:
        self._dependencies["error_describer"] = error_describer
        return self

    def add_user_validators(self, validators: Iterable[DependencyCallable[IUserValidator[TUser]]]) -> Self:
        self._dependencies["user_validators"].items.extend(validators)
        return self

    def add_role_validators(self, validators: Iterable[DependencyCallable[IRoleValidator[TRole]]]) -> Self:
        self._dependencies["role_validators"].items.extend(validators)
        return self

    def add_password_validators(self, validators: Iterable[DependencyCallable[IPasswordValidator[TUser]]]) -> Self:
        self._dependencies["password_validators"].items.extend(validators)
        return self

    def add_token_provider(self, name: str, provider: IUserTwoFactorTokenProvider[TUser]):
        options = self._dependencies["options"]()
        options.tokens.provider_map[name] = provider

    def add_default_token_providers(self):
        options = self._dependencies["options"]()
        self.add_token_provider(options.tokens.DEFAULT_PROVIDER, DataProtectorTokenProvider())
        self.add_token_provider(options.tokens.DEFAULT_EMAIL_PROVIDER, EmailTokenProvider())
        self.add_token_provider(options.tokens.DEFAULT_PHONE_PROVIDER, PhoneNumberTokenProvider())
        self.add_token_provider(options.tokens.DEFAULT_AUTHENTICATION_PROVIDER, AuthenticatorTokenProvider())


def add_identity(
    user_store: DependencyCallable[IUserStore[TUser]],
    role_store: DependencyCallable[IRoleStore[TRole]],
    configure_options: Callable[[IdentityOptions], None] | None = None,
    error_describer: DependencyCallable[IdentityErrorDescriber] = None,
    key_normalizer: DependencyCallable[ILookupNormalizer] = None,
    user_validators: Iterable[DependencyCallable[IUserValidator[TUser]]] = None,
    role_validators: Iterable[DependencyCallable[IRoleValidator[TRole]]] = None,
    password_validators: Iterable[DependencyCallable[IPasswordValidator[TUser]]] = None,
    password_hasher: DependencyCallable[IPasswordHasher[TUser]] = None,
    user_claims_factory: DependencyCallable[IUserClaimsPrincipalFactory[TUser]] = None,
    confirmation: DependencyCallable[IUserConfirmation[TUser]] = None,
    user_manager: DependencyCallable[UserManager[TUser]] = None,
    role_manager: DependencyCallable[RoleManager[TRole]] = None,
    signin_manager: DependencyCallable[SignInManager[TUser]] = None,
    *,
    use_default_validators: bool = True,
    use_default_providers: bool = True,
):
    add_authentication().add_identity_cookies()
    builder = IdentityBuilder(user_store, role_store, configure_options)
    builder.add_error_describer(error_describer or IdentityErrorDescriber)
    builder.add_lookup_normalizer(key_normalizer or UpperLookupNormalizer)
    builder.add_password_hasher(password_hasher or Argon2PasswordHasher)
    builder.add_user_manager(user_manager or UserManager)
    builder.add_role_manager(role_manager or RoleManager)
    builder.add_confirmation(confirmation or DefaultUserConfirmation)
    builder.add_user_claims_factory(user_claims_factory or UserClaimsPrincipalFactory)
    builder.add_signin_manager(signin_manager or SignInManager)
    if use_default_validators:
        user_validators = [UserValidator, *(user_validators if user_validators else ())]
        role_validators = [RoleValidator, *(role_validators if role_validators else ())]
        password_validators = [PasswordValidator, *(password_validators if password_validators else ())]
    builder.add_user_validators(user_validators or ())
    builder.add_role_validators(role_validators or ())
    builder.add_password_validators(password_validators or ())
    if use_default_providers:
        builder.add_default_token_providers()
    return builder
