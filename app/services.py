from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas
from nanoid import generate
import os
import jwt
import random
import math
from enum import Enum
from email.message import EmailMessage
import ssl
import smtplib
import requests
from datetime import datetime
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

class OTPNotGenerated(Exception):
    "Raised when otp is not generated"
    pass

class AadharUserNotFound(Exception):
    "Raised when the aadhar number is not found"
    pass

class ErrorCodes(Enum):
    USER_NOT_FOUND=1
    OTP_NOT_FOUND=2
    INVALID_SIGNATURE_OR_OTP=3
    LISTING_ALREADY_EXISTS=4

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_pending_property(
    pending_property: _schemas.CreateProperty, db: "Session"
) -> _schemas.Property:
    pending_property = _models.Property(**pending_property.dict())
    db.add(pending_property)
    db.commit()
    db.refresh(pending_property)
    return _schemas.Property.from_orm(pending_property)

async def get_all_properties(db: "Session") -> List[_schemas.Property]:
    properties = db.query(_models.Property).all()
    return list(map(_schemas.Property.from_orm, properties))

async def get_all_listings(db: "Session") -> List[_schemas.Listing]:
    listings=db.query(_models.Listings).all()
    return list(map(_schemas.Listing.from_orm, listings))

async def create_user(
    new_user: _schemas.CreateUser, db: "Session"
) -> _schemas.User:
    new_user = _models.User(**new_user.dict(),nonce=math.floor(random.random()*100000000),unique_str=generate(size=8))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return _schemas.User.from_orm(new_user)

async def create_listing(
    new_listing: _models.Listings, db:"Session"
)-> _schemas.Listing:
    result = db.query(_models.Listings).filter(_models.Listings.property_id == new_listing.property_id).one_or_none()
    if result is None:
        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)
        return _schemas.Listing.from_orm(new_listing)
    else:
        return {"error":ErrorCodes.LISTING_ALREADY_EXISTS}

async def login_user(wallet_address:str, signed_nonce: str, db: "Session") -> str:
    nonce = await get_nonce(wallet_address, db=db)
    result = requests.post("http://"+os.environ['UTILS_HOST']+":3000/api/signature",json={"nonce":nonce,"publicAddress":wallet_address,"signature":signed_nonce}).json()
    if("address" in result and  result["address"]==wallet_address.lower()):
        new_nonce = generate(size=8)
        db.query(_models.WalletNonce).filter(_models.WalletNonce.wallet_address == wallet_address). \
            update({_models.WalletNonce.nonce:new_nonce}, synchronize_session = False)
        db.commit()
        #might need to add id here later
        return {"access_token": jwt.encode({"wallet_address":wallet_address,"created":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}, "secret-key", algorithm="HS256")}
    else:
        return {"error": "Failed to authenticate"}

async def update_user(user_details: _schemas.UserDetails, db:"Session") -> str:
    user = db.query(_models.User).filter(_models.User.wallet_address == user_details.wallet_address).first()
    user.first_name = user_details.first_name
    user.last_name = user_details.last_name
    user.id_type = user_details.id_type
    user.id_number = user_details.id_number
    user.email = user_details.email
    user.phone_number = user_details.phone_number
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return{"updated":True}


async def get_status(
    wallet_address: str, db: "Session"
) -> str:
    result = db.query(_models.User). \
        filter(_models.User.wallet_address == wallet_address). \
        one_or_none() 
    print(result)
    if result is not None:
         return {"verified":result.is_verified}
    else:
        return {"verified":False}

async def get_nonce(
    wallet_address: str, db: "Session"
) -> str:
    result = db.query(_models.WalletNonce). \
        filter(_models.WalletNonce.wallet_address == wallet_address). \
        one_or_none()
    if result is None:
          new_entry = _models.WalletNonce(wallet_address=wallet_address,nonce=generate(size=8))
          db.add(new_entry)
          db.commit()
          db.refresh(new_entry)
          return new_entry.nonce
    return result.nonce


async def get_otp(
    aadharno: str, db:"Session") -> str: 
    result = db.query(_models.AadharUser). \
        filter(_models.AadharUser.UID == aadharno). \
        one_or_none()
    if result is None:
        return{"error":True}
    result.otp  =  generate('1234567890',size=6)
    db.commit()
    db.refresh(result)
    em_sender='rentodapp@gmail.com'
    em_receiver=result.EmailID
    password='rpeshqbyiwoazdob'
    subject= 'Your OTP for Aadhar verification'
    body=result.otp
    em=EmailMessage();
    em['From']=em_sender
    em['To']=em_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(em_sender,password)
        smtp.sendmail(em_sender,em_receiver,em.as_string())
    return{"otp":result.otp}
    # print(result) 

async def check_otp(
    aadharno: str, db:"Session") -> str: 
    result = db.query(_models.AadharUser). \
        filter(_models.AadharUser.UID == aadharno). \
        one_or_none()
    if result is None:
        return {"error":ErrorCodes.USER_NOT_FOUND}
    elif result.otp is None:
        return {"error":ErrorCodes.OTP_NOT_FOUND}
    else:
        return {"otp":result.otp}

async def connect_aadhar(wallet_address:str, signed_nonce: str, aadharno: str, db: "Session") -> str:
    otp = await check_otp(aadharno, db=db)
    if "error" in otp:
        return otp
    result = requests.post("http://"+os.environ['UTILS_HOST']+":3000/api/signature",json={"nonce":otp["otp"],"publicAddress":wallet_address,"signature":signed_nonce}).json()
    print(result)
    print(otp["otp"])
    if("address" in result and  result["address"]==wallet_address.lower()):
        # new_nonce = math.floor(random.random()*100000000)
        # db.query(_models.User).filter(_models.User.wallet_address == wallet_address). \
        #     update({_models.User.nonce:new_nonce}, synchronize_session = False)
        # db.commit()
        # #might need to add id here later
        result = db.query(_models.AadharConnect). \
        filter(_models.AadharConnect.wallet_address == wallet_address). \
        one_or_none()
        if result is None:
            conn_obj = _models.AadharConnect(wallet_address=wallet_address,UID=aadharno)
            db.add(conn_obj)
            db.commit()
        return {"access_token": jwt.encode({"wallet_address":wallet_address,"created":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}, "secret-key", algorithm="HS256")}
    else:
        return {"error": ErrorCodes.INVALID_SIGNATURE_OR_OTP}

async def is_connected(wallet_address:str, db: "Session") -> dict:
    result = db.query(_models.AadharConnect). \
        filter(_models.AadharConnect.wallet_address == wallet_address). \
        one_or_none()
    if result is None:
        return {"found":False}
    else:
        result = db.query(_models.AadharUser).join(
        _models.AadharConnect, _models.AadharUser.UID == _models.AadharConnect.UID
        ).filter(_models.AadharConnect.wallet_address == wallet_address). \
        one_or_none()
        return {"found":True,"endsWith":result.UID[-4:],"firstName":result.FirstName,"lastName":result.LastName,"email":result.EmailID,"PhoneNumber":result.PhoneNumber}


async def disconnect(wallet_address:str, db: "Session") -> dict:
    result = db.query(_models.AadharConnect). \
        filter(_models.AadharConnect.wallet_address == wallet_address).delete()
    db.commit()
    print(result)
    if result is None:
        return {"found":False}
    else: 
        return {"found":True}

