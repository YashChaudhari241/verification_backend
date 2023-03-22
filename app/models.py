import datetime as _dt
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric, DECIMAL
from sqlalchemy.orm import relationship
import database as _database

# #OLD 
# class Property(_database.Base):
#     __tablename__ = "properties"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer,ForeignKey('users.id'),
#         nullable=False)
#     date_created = Column(DateTime, default=_dt.datetime.utcnow)
#     property_address = Column(String)
#     is_verified = Column(Boolean)
#     unique_str = Column(String)
#     def __repr__(self):
#         return f"Property({self.id!r}, {self.unique_str!r})"

# class User(_database.Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String, index=True)
#     last_name = Column(String, index=True)
#     email = Column(String, index=True, unique=True)
#     phone_number = Column(String, unique=True)
#     id_type = Column(Integer)
#     id_number = Column(String)
#     date_created = Column(DateTime, default=_dt.datetime.utcnow)
#     wallet_address = Column(String)
#     nonce = Column(Integer)
#     is_verified = Column(Boolean)
#     unique_str = Column(Integer)
#     properties = relationship('Property', backref="owner")
#     def __repr__(self):
#         return f"User({self.id!r}, {self.wallet_address!r},{self.nonce!r})"

class AadharUser(_database.Base):
    __tablename__ = "aadhar"
    UID = Column(String , primary_key=True,index=True)
    FirstName = Column(String,index=True, nullable=False)
    LastName = Column(String,index=True, nullable = False)
    DOB = Column(String, nullable=False)
    Gender = Column(String, nullable= False)
    Address = Column(String)
    Pincode = Column(String)
    PhoneNumber = Column(String)
    EmailID = Column(String)
    otp = Column(String)
    wallet_address = relationship('AadharConnect', backref="wallet_owner")
    properties = relationship('PropertyOwnership', backref="owner")
    def __repr__(self):
        return f"AadharUser({self.UID!r}, {self.FirstName!r},{self.LastName!r})"

#Latest
class PropertyOwnership(_database.Base):
    __tablename__ = "property"
    SaleDeedNumber = Column(String, primary_key=True)
    MahaRERANumber = Column(String)
    UID = Column(String,ForeignKey('aadhar.UID'),
        nullable=False)
    Area= Column(String)
    Address= Column(String)
    Pincode= Column(String)
    listing = relationship('Listings', backref="record")
    def __repr__(self):
        return f"Property({self.SaleDeedNumber!r}, {self.UID!r})"

class AadharConnect(_database.Base):
    __tablename__ = "aadhar_wallet"
    UID = Column(String,ForeignKey('aadhar.UID'),
        primary_key=True)
    wallet_address = Column(String, nullable=False)
    def __repr__(self):
        return f"AadharConnect({self.UID!r}, {self.wallet_address!r})"

class Listings(_database.Base):
    __tablename__ = "listings"
    property_id = Column(String,ForeignKey('property.SaleDeedNumber'), primary_key=True)
    deposit = Column(DECIMAL(22,18))
    eth_rent = Column(DECIMAL(22,18))
    metadata_id  = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    bhk = Column(DECIMAL(3,1))
    bathrooms = Column(Integer)
    details = Column(String)
    bhk:Column(Integer)
    bathrooms: Column(Integer)
    furnish_status: Column(String)
    hasGym: Column(Boolean)
    isPetFriendly: Column(Boolean)
    hasPark: Column(Boolean)
    hasParking: Column(Boolean)
    hasPool: Column(Boolean)
    hasBalcony: Column(Boolean)
    hasCameras: Column(Boolean)
    isSmartHome: Column(Boolean)
    listing_index= Column(Integer)

class WalletNonce(_database.Base):
    __tablename__="wallet_nonce"
    wallet_address = Column(String, primary_key=True)
    nonce = Column(String)