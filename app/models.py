import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy.orm import relationship
import database as _database

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
