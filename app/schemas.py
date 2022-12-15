
import datetime as _dt
import pydantic as _pydantic


class _BaseProperty(_pydantic.BaseModel):
    user_id: int
    property_address: str
    property_docs: str

class Property(_BaseProperty):
    id: int
    is_verified: bool
    unique_str: str
    date_created: _dt.datetime
    class Config:
        orm_mode = True

class CreateProperty(_BaseProperty):
    pass

class _BaseUser(_pydantic.BaseModel):
    wallet_address: str

class User(_BaseUser):
    id: int
    first_name: str
    last_name: str
    id_type: int
    id_number: str
    email: str
    phone_number: str
    is_verified: bool
    unique_str: str
    date_created: _dt.datetime
    nonce: int
    class Config:
        orm_mode = True

class CreateUser(_BaseUser):
    pass