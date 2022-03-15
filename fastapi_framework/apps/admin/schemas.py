from apps.extensions import RequestBase

class CreateUserRequest(RequestBase):
    username: str
    password: str