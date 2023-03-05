import models as _models
from typing import TYPE_CHECKING
from sqlalchemy import select
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
async def get_properties(wallet_address:str, db: "Session"):
    # stmt = select(_models.PropertyOwnership).join(_models.PropertyOwnership.UID).join(_models.)
    # print(result)
    # r = db.execute(result).fetchone()
    # print(r)
    return True
