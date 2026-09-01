"""CreateUser use case. Imports only from the domain layer."""

from ...domain import User, ValidationError
from ..dto import CreateUserRequest, UserResponse


class CreateUser:
    """Callable use case: create a User from a request DTO."""

    def __call__(self, request: CreateUserRequest) -> UserResponse:
        if not request.name.strip():
            raise ValidationError("name must not be empty")
        if not request.email.strip():
            raise ValidationError("email must not be empty")
        user = User(name=request.name, email=request.email)
        return UserResponse(id=user.id, name=user.name, email=user.email)
