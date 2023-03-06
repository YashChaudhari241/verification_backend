import models as _models
from typing import TYPE_CHECKING
from sqlalchemy import select
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
async def get_properties(wallet_address:str, db: "Session"):
    result2 = db.query(_models.PropertyOwnership).join(
        _models.AadharConnect, _models.PropertyOwnership.UID == _models.AadharConnect.UID
        ).filter(_models.AadharConnect.wallet_address == wallet_address).all()
    print(result2)
    return result2

async def get_listings(wallet_address:str, db: "Session"):
    result2 = db.query(_models.Listings).join(
        _models.PropertyOwnership, _models.Listings.property_id == _models.PropertyOwnership.SaleDeedNumber
        ).join(
        _models.AadharConnect, _models.PropertyOwnership.UID == _models.AadharConnect.UID
        ).filter(_models.AadharConnect.wallet_address == wallet_address,_models.Listings.metadata_id != None).all()
    print(result2)
    return result2

async def unlist_property(wallet_address:str, property_id:str, db: "Session"):
    result = db.query(_models.PropertyOwnership).join(
        _models.AadharConnect, _models.PropertyOwnership.UID == _models.AadharConnect.UID
        ).join(
        _models.Listings, _models.PropertyOwnership.SaleDeedNumber == _models.Listings.property_id
        ).filter(_models.AadharConnect.wallet_address == wallet_address,_models.Listings.property_id == property_id).one_or_none()
    if(result):
        db.query(_models.Listings).filter(_models.PropertyOwnership.SaleDeedNumber == property_id).delete()
        db.commit()
    print(result)
    if result is None:
        return {"found":False}
    else:
        return {"found":True}

async def update_listing_index(wallet_address:str, property_id:str,index:int,db: "Session"):
    result =  db.query(_models.Listings).join(
        _models.PropertyOwnership, _models.Listings.property_id == _models.PropertyOwnership.SaleDeedNumber
        ).join(
        _models.AadharConnect, _models.PropertyOwnership.UID == _models.AadharConnect.UID
        ).filter(_models.AadharConnect.wallet_address == wallet_address,_models.Listings.metadata_id != None).one_or_none()
    if(result):
        result.listing_index = index
        db.commit()
    else:
        return{"error":"not found"}