from schemas import SearchQuery
from models import Listings, PropertyOwnership


def build_query(base_stmt, query: SearchQuery, db):
    print(query.hasCameras)
    listing_attributes = ["bathrooms", "hasBalcony", "hasCameras",
                          "furnish_status", "isSmartHome", "hasGym", "hasParking", "bhk", "hasPool", "isPetFriendly","hasPark"]
    property_attributes = ["City", "State"]

    for attribute in property_attributes:
        if attribute in query.dict() and query.dict()[attribute] is not None:
            base_stmt = base_stmt.where(
                getattr(PropertyOwnership, attribute) == getattr(query, attribute))

    for attribute in listing_attributes:
        if attribute in query.dict() and query.dict()[attribute] is not None:
            base_stmt = base_stmt.where(
                getattr(Listings, attribute) == getattr(query, attribute))

    print("Q",query.dict())
    bhk_min = query.dict().get("bhk_min", 0)
    print("BHK",bhk_min)
    rent_max = query.dict()["rent_max"] if query.dict()[
        "rent_max"] is not None else 500
    rent_min = query.dict()["rent_min"] if query.dict()[
        "rent_min"] is not None else 0
    dep_max = query.dict()["dep_max"] if query.dict()[
        "dep_max"] is not None else 500
    dep_min = query.dict()["dep_min"] if query.dict()[
        "dep_min"] is not None else 0
    base_stmt = base_stmt.where(Listings.eth_rent <= rent_max, Listings.eth_rent >=
                                rent_min, Listings.deposit >= dep_min, Listings.deposit <= dep_max, Listings.bhk>=bhk_min)
    listings = db.execute(base_stmt)
    # result = [row._mapping for row in listings]
    result = []
    for row in listings:
        result.append({"Property": remove_private(
            row.PropertyOwnership.__dict__), "Listing": row.Listings.__dict__})
    return result


def remove_private(og_dict):
    to_remove = ["UID"]
    return {x: og_dict[x] for x in og_dict if x not in to_remove}
