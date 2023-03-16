from typing import TYPE_CHECKING, List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import models as _models
from fastapi.middleware.cors import CORSMiddleware
import schemas as _schemas
import services as _services
from nanoid import generate
import listing_services as _listing_services
import aiofiles
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
import os
app = _fastapi.FastAPI()
origins=[
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/apply/", response_model=_schemas.Property)
async def create_contact(
    property: _schemas.CreateProperty,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_pending_property(pending_property=property, db=db)

@app.get('/api/get_all_properties', response_model=List[_schemas.Property])
async def get_contacts(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_properties(db=db)

@app.get('/api/get_all_listings', response_model=List[_schemas.Listing])
async def get_listings(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_listings(db=db)

@app.get('/api/get_nonce', response_model=str)
async def get_nonce(public_address: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_nonce(wallet_address=public_address, db=db)

@app.post('/api/authenticate')
async def auth(auth : _schemas.AuthenticateUser,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.login_user(wallet_address=auth.public_address, signed_nonce=auth.signed_nonce, db=db)

@app.post('/api/update_details')
async def update_user(user_details : _schemas.UserDetails,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_user(user_details, db=db)

@app.get('/api/get_status')
async def get_status(public_address: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_user(public_address, db=db)

@app.post('/api/get_otp', response_model=dict)
async def get_otp(aadharBody: _schemas.JustAadhar,
    response: _fastapi.Response, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    result = await _services.get_otp(aadharBody.aadharno, db=db)
    if "error" in result: 
        # response.status_code = _fastapi.status.HTTP_400_BAD_REQUEST
        return {"error":"Invalid Details"}
        raise _fastapi.HTTPException(status_code=404, detail="Invalid Details")
    else:
        return result

@app.post('/api/authenticate_user')
async def auth_user(auth : _schemas.AuthenticateAadhar,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.connect_aadhar(wallet_address=auth.public_address, signed_nonce=auth.signed_nonce,aadharno= auth.aadharno, db=db)

@app.get('/api/is_connnected')
async def is_conn(wallet_address:str,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.is_connected(wallet_address=wallet_address, db=db)

@app.post('/api/create_listing')
async def create_listing(uploaded_files: List[_fastapi.UploadFile],
deposit:str = _fastapi.Form(),eth_rent:str =_fastapi.Form(),
property_id:str =_fastapi.Form(),details:str =_fastapi.Form(),
longitude:str =_fastapi.Form(),
latitude:str =_fastapi.Form(),
db: _orm.Session = _fastapi.Depends(_services.get_db)):
    # print([file.filename for file in uploaded_files])
    unique_str = generate(size=8)
    os.makedirs(f"files/{unique_str}")
    for file in uploaded_files:
        async with aiofiles.open(f"files/{unique_str}/{file.filename}", 'wb') as out_file:
            while content := await file.read(1024):  # async read chunk
                await out_file.write(content)
    return await _services.create_listing(new_listing=_models.Listings(property_id=property_id,
    deposit=float(deposit),eth_rent=float(eth_rent),metadata_id=unique_str,details=details,
    longitude=float(longitude),latitude=float(latitude)),db=db)

@app.post('/api/disconnect_aadhar')
async def disconnect(address:_schemas.JustWallet,
db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.disconnect(wallet_address=address.wallet_address,db=db)


@app.post('/api/get_properties')
async def get_properties(address:_schemas.JustWallet,db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _listing_services.get_properties(wallet_address=address.wallet_address,db=db)

@app.post('/api/get_listings')
async def get_my_listings(address:_schemas.JustWallet,db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _listing_services.get_listings(wallet_address=address.wallet_address,db=db)

@app.post('/api/unlist')
async def unlist(data:_schemas.UnlistProp,
db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _listing_services.unlist_property(wallet_address=data.wallet_address,property_id=data.property_id,db=db)

@app.post('/api/update_index')
async def update(data:_schemas.UpdateListing,
db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _listing_services.update_listing_index(wallet_address=data.wallet_address,property_id=data.property_id,index=data.index,db=db)
