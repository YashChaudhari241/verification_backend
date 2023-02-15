from typing import TYPE_CHECKING, List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
import schemas as _schemas
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()
origins=[
    "http://localhost:3000"
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

@app.get('/api/get_nonce', response_model=int)
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

@app.post('/api/get_otp')
async def get_status(aadharno: str,
    response: _fastapi.Response, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    result = await _services.get_otp(aadharno, db=db)
    if result.error: 
        # response.status_code = _fastapi.status.HTTP_400_BAD_REQUEST
        return {"error":"Invalid Details"}
        raise _fastapi.HTTPException(status_code=404, detail="Invalid Details")
    else:
        return result

@app.post('/authenticate_user')
async def auth_user(auth : _schemas.AuthenticateAadhar,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.login_user(wallet_address=auth.public_address, signed_nonce=auth.signed_nonce,aadharno= auth.aadharno, db=db)