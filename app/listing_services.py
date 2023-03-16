from models import Listings, PropertyOwnership, AadharConnect, AadharUser
from typing import TYPE_CHECKING
from sqlalchemy import select,delete
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
async def get_properties(wallet_address:str, db: "Session"):
    result2 = db.query(PropertyOwnership).join(
        AadharConnect, PropertyOwnership.UID == AadharConnect.UID
        ).filter(AadharConnect.wallet_address == wallet_address).all()
    print(result2)
    return result2

async def get_listings(wallet_address:str, db: "Session"):
    stmt = select(Listings,PropertyOwnership).select_from(PropertyOwnership).join(Listings).join(AadharConnect, AadharConnect.UID == PropertyOwnership.UID).where(AadharConnect.wallet_address==wallet_address)
    print(stmt)
    listing = db.scalars(stmt).all()
    print(listing)
    return listing

async def unlist_property(wallet_address:str, property_id:str, db: "Session"):
    # result1 = db.query(AadharConnect). \
    #     filter(AadharConnect.wallet_address == wallet_address). \
    #     one_or_none()
    # if result1 is None:
    #     return {"found":False}
    # result = db.query(Listings).join(
    #     PropertyOwnership, Listings.property_id == PropertyOwnership.SaleDeedNumber
    #     ).filter(PropertyOwnership.SaleDeedNumber == property_id).one_or_none()
    
    # if result is None:
    #     return {"found":False}
    # else:
    #     if(result.UID == result1.UID):
    #         result.delete()
    #         db.commit()
    #         return {"found":True}
    #     else:
    #         return {"error": "Unauthorized"}
    stmt = select(Listings).select_from(PropertyOwnership).join(Listings).join(AadharConnect, AadharConnect.UID == PropertyOwnership.UID).where(AadharConnect.wallet_address==wallet_address).where(Listings.property_id == property_id)
    print(stmt)
    listing = db.scalars(stmt).first()
    print(listing)
    if listing is not None:
        db.delete(listing)
        db.commit()
        return{"found":True}
    else:
        return{"found":False}


async def update_listing_index(wallet_address:str, property_id:str,index:int,db: "Session"):
    result =  db.query(Listings).join(
        PropertyOwnership, Listings.property_id == PropertyOwnership.SaleDeedNumber
        ).join(
        AadharConnect, PropertyOwnership.UID == AadharConnect.UID
        ).filter(AadharConnect.wallet_address == wallet_address,Listings.metadata_id != None).one_or_none()
    if(result):
        result.listing_index = index
        db.commit()
    else:
        return{"error":"not found"}