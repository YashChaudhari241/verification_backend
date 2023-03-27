from models import Listings, PropertyOwnership, AadharConnect, AadharUser
from typing import TYPE_CHECKING
from schemas import AutoCompleteQuery, SearchQuery
import json
from query_builder import build_query
from sqlalchemy import select, delete
# import csv
f = open('cities.json')
cities_data = json.load(f)
# file = open('Giants.csv', mode ='r')
# reading the CSV file
# cities_data = csv.DictReader(file)
if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def get_properties(wallet_address: str, db: "Session"):
    result2 = db.query(PropertyOwnership).join(
        AadharConnect, PropertyOwnership.UID == AadharConnect.UID
    ).filter(AadharConnect.wallet_address == wallet_address).all()
    print(result2)
    return result2


async def get_listings(wallet_address: str, db: "Session"):
    stmt = select(Listings, PropertyOwnership).select_from(PropertyOwnership).join(Listings).join(
        AadharConnect, AadharConnect.UID == PropertyOwnership.UID).where(AadharConnect.wallet_address == wallet_address)
    print(stmt)
    listing = db.scalars(stmt).all()
    print(listing)
    return listing


async def unlist_property(wallet_address: str, property_id: str, db: "Session"):
    stmt = select(Listings).select_from(PropertyOwnership).join(Listings).join(AadharConnect, AadharConnect.UID ==
                                                                               PropertyOwnership.UID).where(AadharConnect.wallet_address == wallet_address).where(Listings.property_id == property_id)
    print(stmt)
    listing = db.scalars(stmt).first()
    print(listing)
    if listing is not None:
        db.delete(listing)
        db.commit()
        return {"found": True}
    else:
        return {"found": False}


async def update_listing_index(wallet_address: str, property_id: str, index: int, db: "Session"):
    result = db.query(Listings).join(
        PropertyOwnership, Listings.property_id == PropertyOwnership.SaleDeedNumber
    ).join(
        AadharConnect, PropertyOwnership.UID == AadharConnect.UID
    ).filter(AadharConnect.wallet_address == wallet_address, Listings.metadata_id != None).one_or_none()
    if (result):
        result.listing_index = index
        db.commit()
    else:
        return {"error": "not found"}


async def get_autocomplete(query: AutoCompleteQuery):
    result = []
    priority_index = 0
    count = 0
    for i in cities_data:
        if query.searchQuery.lower() in i["name"].lower():
            count = count + 1
            if i["name"].lower().startswith(query.searchQuery.lower()):
                result.insert(priority_index, i)
                priority_index = priority_index + 1
            else:
                result.append(i)
            if (count == 5):
                break
    return result


async def search_listing(query: SearchQuery, db: "Session"):
    stmt = select(Listings, PropertyOwnership).join(PropertyOwnership)
    listings = build_query(base_stmt=stmt, query=query, db=db)
    return listings
