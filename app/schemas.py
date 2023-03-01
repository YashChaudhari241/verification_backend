
import datetime as _dt
import pydantic as _pydantic


class _BaseProperty(_pydantic.BaseModel):
    user_id: int
    property_address: str
    property_docs: str
class _BaseListing(_pydantic.BaseModel):
    pass
class Property(_BaseProperty):
    id: int
    is_verified: bool
    unique_str: str
    date_created: _dt.datetime
    class Config:
        orm_mode = True

class Listing(_BaseListing):
    property_id: str
    deposit: int
    eth_rent: float
    metadata_id: str
    latitude: float
    longitude: float
    details: str
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

class CreateListing(_BaseListing):
    pass

class AuthenticateUser(_pydantic.BaseModel):
    signed_nonce: str
    public_address: str

class AuthenticateAadhar(_pydantic.BaseModel):
    signed_nonce: str
    aadharno: str
    public_address: str

class UserDetails(_pydantic.BaseModel):
    first_name: str
    last_name: str
    id_type: int
    id_number: str
    email: str
    phone_number: str
    wallet_address: str

class AadharUser(_pydantic.BaseModel):
    pass

class PropertyOwnership(_pydantic.BaseModel):
    pass

class WalletAadharConnection(_pydantic.BaseModel):
    pass

class PropertyListing(_pydantic.BaseModel):
    pass

class JustAadhar(_pydantic.BaseModel):
    aadharno: str

class JustWallet(_pydantic.BaseModel):
    wallet_address:str