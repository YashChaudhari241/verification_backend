from models import Listings, PropertyOwnership, AadharConnect, AadharUser
from typing import TYPE_CHECKING
from schemas import AutoCompleteQuery, ListingQuery, SearchQuery
import PIL
import json
from query_builder import remove_private
import os
# from main import accepted_content
from query_builder import build_query
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select, delete, update
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
    return result2


async def get_listings(wallet_address: str, db: "Session"):
    stmt = select(Listings, PropertyOwnership).select_from(PropertyOwnership).join(Listings).join(
        AadharConnect, AadharConnect.UID == PropertyOwnership.UID).where(AadharConnect.wallet_address == wallet_address).where(Listings.delisted == False)
    listing = db.scalars(stmt).all()
    return listing


async def unlist_property(wallet_address: str, metadata_id: str, db: "Session"):
    stmt = select(Listings).select_from(PropertyOwnership).join(Listings).join(AadharConnect, AadharConnect.UID ==
                                                                               PropertyOwnership.UID).where(AadharConnect.wallet_address == wallet_address).where(Listings.metadata_id == metadata_id)
    listing = db.scalars(stmt).first()
    if listing is not None:
        listing.delisted = True
        db.commit()
        return {"found": True}
    else:
        return {"found": False}


async def update_listing_index(wallet_address: str, property_id: str, index: int, db: "Session"):
    result = db.query(Listings).join(
        PropertyOwnership, Listings.property_id == PropertyOwnership.SaleDeedNumber
    ).join(
        AadharConnect, PropertyOwnership.UID == AadharConnect.UID
    ).filter(AadharConnect.wallet_address == wallet_address, Listings.metadata_id == property_id).one_or_none()
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


async def get_listing(metadata: str, db):
    stmt = select(Listings, PropertyOwnership).join(
        PropertyOwnership).where(Listings.metadata_id == metadata)
    listing = db.execute(stmt).fetchone()
    return listing


async def delist(metadata_id: str, db):
    stmt = update(Listings).\
        where(Listings.metadata_id == metadata_id).\
        values(delisted=True)
    db.execute(stmt)
    db.commit()
    return {"message": f"Details for listing {metadata_id} updated successfully."}


async def get_given_listings(query: ListingQuery, db):
    stmt = select(Listings, PropertyOwnership).join(
        PropertyOwnership).where(Listings.listing_index.in_(query.listingIndices))
    listing = db.execute(stmt)
    result = []
    for row in listing:
        result.append({"Property": remove_private(
            row.PropertyOwnership.__dict__), "Listing": row.Listings.__dict__})
    return result


async def get_listing_thumbnail(metadata: str, compressed: bool):
    if compressed:
        for file in os.listdir(f"files/{metadata}/"):
            if file.startswith('c_'):
                return FileResponse(f"files/{metadata}/{file}")
        raise HTTPException(409, detail="No thumbnail found to return")


async def get_total_images(metadata: str):
    count = 0
    for file in os.listdir(f"files/{metadata}/"):
        if (file[0].isdigit()):
            count = count+1
    return count


async def get_listing_images(metadata: str, id: int):

    for file in os.listdir(f"files/{metadata}/"):
        if (file.startswith(str(id))):
            return FileResponse(f"files/{metadata}/{file}")
    #         imglist=[]
    #         imglist.append((f"files/{metadata}/{file}"))
    # for i in imglist:
    #     return FileResponse(i)
    raise HTTPException(409, detail="No thumbnail found to return")
