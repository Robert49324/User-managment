from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserModel(_message.Message):
    __slots__ = ("id", "name", "surname", "username", "email", "role", "group", "is_blocked")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    IS_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    surname: str
    username: str
    email: str
    role: str
    group: int
    is_blocked: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[str] = ..., group: _Optional[int] = ..., is_blocked: bool = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserModel
    def __init__(self, user: _Optional[_Union[UserModel, _Mapping]] = ...) -> None: ...
