from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas
from nanoid import generate
import os
import jwt
import random
import math
import requests
from datetime import datetime
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

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

async def create_user(
    new_user: _schemas.CreateUser, db: "Session"
) -> _schemas.User:
    new_user = _models.User(**new_user.dict(),nonce=math.floor(random.random()*100000000),unique_str=generate(size=8))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return _schemas.User.from_orm(new_user)

async def login_user(wallet_address:str, signed_nonce: str, db: "Session") -> str:
    nonce = await get_nonce(wallet_address, db=db)
    result = requests.post("http://"+os.environ['UTILS_HOST']+":3000/api/signature",json={"nonce":nonce,"publicAddress":wallet_address,"signature":signed_nonce}).json()
    print(result)
    print(nonce)
    if("address" in result and  result["address"]==wallet_address.lower()):
        new_nonce = math.floor(random.random()*100000000)
        db.query(_models.User).filter(_models.User.wallet_address == wallet_address). \
            update({_models.User.nonce:new_nonce}, synchronize_session = False)
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
) -> int:
    result = db.query(_models.User). \
        filter(_models.User.wallet_address == wallet_address). \
        one_or_none() 
    print(result)  
    if result is None:
          new_user = _models.User(wallet_address=wallet_address,nonce=math.floor(random.random()*100000000),unique_str=generate(size=8))
          db.add(new_user)
          db.commit()
          db.refresh(new_user)
          return new_user.nonce
    return result.nonce
