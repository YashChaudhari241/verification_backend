
import datetime as _dt
import pydantic as _pydantic
from typing import Optional, List


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
    deposit: float
    eth_rent: float
    metadata_id: str
    latitude: float
    longitude: float
    details: str
    bhk: int
    bathrooms: int
    furnish_status: str
    hasGym: bool
    isPetFriendly: bool
    hasPark: bool
    hasParking: bool
    hasPool: bool
    hasBalcony: bool
    hasCameras: bool
    isSmartHome: bool

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
    eth_rent: str
    deposit: str
    details: str
    property_id: str
    latitude: str
    longitude: str
    bhk: float
    bathrooms: int
    furnish_status: int
    hasGym: bool
    isPetFriendly: bool
    hasPark: bool
    hasParking: bool
    hasPool: bool
    hasBalcony: bool
    hasCameras: bool
    isSmartHome: bool
    pass

    def __repr__(self):
        return f"Listing_data({self.eth_rent!r}, {self.property_id!r},{self.details!r})"


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


class UnlistProp(_pydantic.BaseModel):
    wallet_address: str
    property_id: str


class UpdateListing(_pydantic.BaseModel):
    wallet_address: str
    property_id: str
    index: int


class JustAadhar(_pydantic.BaseModel):
    aadharno: str


class JustWallet(_pydantic.BaseModel):
    wallet_address: str


class AutoCompleteQuery(_pydantic.BaseModel):
    searchQuery: str


class ListingQuery(_pydantic.BaseModel):
    listingIndices: List[int]


class SearchQuery(_pydantic.BaseModel):
    City: Optional[str]
    State: Optional[str]
    rent_max: Optional[float]
    rent_min: Optional[float]
    dep_max: Optional[float]
    dep_min: Optional[float]
    bhk_min: Optional[float]
    hasParking: Optional[bool]
    hasCameras: Optional[bool]
    hasGym: Optional[bool]
    hasPool: Optional[bool]
    hasPark: Optional[bool]
    hasBalcony: Optional[bool]
    isPetFriendly: Optional[bool]
    isSmartHome: Optional[bool]
