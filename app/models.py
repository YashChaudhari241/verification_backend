import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy.orm import relationship
import database as _database

#OLD 
class Property(_database.Base):
    __tablename__ = "properties"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer,_sql.ForeignKey('users.id'),
        nullable=False)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    property_address = _sql.Column(_sql.String)
    is_verified = _sql.Column(_sql.Boolean)
    unique_str = _sql.Column(_sql.String)
    def __repr__(self):
        return f"Property({self.id!r}, {self.unique_str!r})"

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    phone_number = _sql.Column(_sql.String, unique=True)
    id_type = _sql.Column(_sql.Integer)
    id_number = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    wallet_address = _sql.Column(_sql.String)
    nonce = _sql.Column(_sql.Integer)
    is_verified = _sql.Column(_sql.Boolean)
    unique_str = _sql.Column(_sql.Integer)
    properties = relationship('Property', backref="owner")
    def __repr__(self):
        return f"User({self.id!r}, {self.wallet_address!r},{self.nonce!r})"

class AadharUser(_database.Base):
    __tablename__ = "aadhar"
    UID = _sql.Column(_sql.String , primary_key=True,index=True)
    FirstName = _sql.Column(_sql.String,index=True, nullable=False)
    LastName = _sql.Column(_sql.String,index=True, nullable = False)
    DOB = _sql.Column(_sql.String, nullable=False)
    Gender = _sql.Column(_sql.String, nullable= False)
    Address = _sql.Column(_sql.String)
    Pincode = _sql.Column(_sql.String)
    PhoneNumber = _sql.Column(_sql.String)
    EmailID = _sql.Column(_sql.String)
    otp = _sql.Column(_sql.String)
    wallet_address = relationship('AadharConnect', backref="wallet_owner")
    properties = relationship('PropertyOwnership', backref="owner")
    def __repr__(self):
        return f"AadharUser({self.UID!r}, {self.FirstName!r},{self.LastName!r})"

#Latest
class PropertyOwnership(_database.Base):
    __tablename__ = "property"
    SaleDeedNumber = _sql.Column(_sql.String, primary_key=True)
    MahaRERANumber = _sql.Column(_sql.String)
    UID = _sql.Column(_sql.String,_sql.ForeignKey('aadhar.UID'),
        nullable=False)
    Area= _sql.Column(_sql.String)
    Address= _sql.Column(_sql.String)
    Pincode= _sql.Column(_sql.String)
    unique_str = _sql.Column(_sql.String)
    listing = relationship('Listings', backref="record")
    def __repr__(self):
        return f"Property({self.SaleDeedNumber!r}, {self.unique_str!r}, {self.UID!r})"

class AadharConnect(_database.Base):
    __tablename__ = "aadhar_wallet"
    UID = _sql.Column(_sql.String,_sql.ForeignKey('aadhar.UID'),
        primary_key=True)
    wallet_address = _sql.Column(_sql.String, nullable=False)
    def __repr__(self):
        return f"AadharConnect({self.UID!r}, {self.wallet_address!r})"

class Listings(_database.Base):
    __tablename__ = "listings"
    property_id = _sql.Column(_sql.String,_sql.ForeignKey('property.SaleDeedNumber'), primary_key=True)
    deposit = _sql.Column(_sql.Integer)
    eth_rent = _sql.Column(_sql.DECIMAL(22,18))
    metadata_id  = _sql.Column(_sql.String)
    latitude = _sql.Column(_sql.Numeric)
    longitude = _sql.Column(_sql.Numeric)
    details = _sql.Column(_sql.String)

class WalletNonce(_database.Base):
    __tablename__="wallet_nonce"
    wallet_address = _sql.Column(_sql.String, primary_key=True)
    nonce = _sql.Column(_sql.String)