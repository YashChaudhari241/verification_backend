from schemas import SearchQuery
from models import Listings, PropertyOwnership


def build_query(base_stmt, query: SearchQuery, db):
    print(query.hasCameras)
    listing_attributes = ["bathrooms", "hasBalcony", "hasCameras",
                          "furnish_status", "isSmartHome", "hasGym", "hasParking", "bhk", "hasPool"]
    property_attributes = ["City", "State"]

    for attribute in property_attributes:
        if attribute in query.dict() and query.dict()[attribute] is not None:
            base_stmt = base_stmt.where(
                getattr(PropertyOwnership, attribute) == getattr(query, attribute))

    for attribute in listing_attributes:
        if attribute in query.dict() and query.dict()[attribute] is not None:
            base_stmt = base_stmt.where(
                getattr(Listings, attribute) == getattr(query, attribute))

    print(base_stmt)
    rent_max = query.rent_max if "rent_max" in query else 500
    rent_min = query.rent_min if "rent_min" in query else 0
    dep_max = query.dep_max if "dep_max" in query else 500
    dep_min = query.dep_min if "dep_min" in query else 0
    base_stmt = base_stmt.where(Listings.eth_rent <= rent_max, Listings.eth_rent >=
                                rent_min, Listings.deposit >= dep_min, Listings.deposit <= dep_max)
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
