from datetime import datetime, timedelta, timezone
from src import *


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated, Union
from pydantic import BaseModel
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = '94229c6c19e9ae7adebf61f8e7565d1990727ce8f13b8f11bf1aa3e481a94947'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#hashed_password = secret

USERS = {
    'user1' : {'username' : 'user1', 'name' : 'name1', 'hashed_password' : bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt()), 'scope' : 'user', 'disabled' : False},
    'user2' : {'username' : 'user2', 'name' : 'name2', 'hashed_password' : bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt()), 'scope' : 'admin', 'disabled' : False},
    'user3' : {'username' : 'user3', 'name' : 'name3', 'hashed_password' : bcrypt.hashpw('password3'.encode('utf-8'), bcrypt.gensalt()), 'scope' : 'user', 'disabled' : True},
    'user4' : {'username' : 'user4', 'name' : 'name4', 'hashed_password' : bcrypt.hashpw('password4'.encode('utf-8'), bcrypt.gensalt()), 'scope' : 'admin', 'disabled' : False}
}

class User(BaseModel):
    username : str
    name : Union[str, None] = None
    scope : Union[str | None] = None
    disabled : Union[bool, None] = None

class UserInDB(User):
    hashed_password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login',
                                     description = 'token pour authentifier l\'user lors de la conexion')

app = FastAPI()



def get_password_hash(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    # Vérifier que hashed_password est un objet bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')  # Convertir en bytes si c'est un string

    # Vérification avec bcrypt
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username : str, password : str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    print(f"Token received: {token}")

    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = 'Could not validate credentials',
                                          headers = {'WWW-authenticate': "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(USERS, username = token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user : Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code = 400, detail = 'Inactive user')
    return current_user


@app.get('/')
async def welcome_page():
    a = welcome()
    return a


@app.post('/login')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = authenticate_user(USERS, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {'sub' : user.username},
                                       expires_delta = access_token_expires)

    return Token(access_token = access_token, token_type = 'bearer')

@app.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


#cette page doit être accessible qu'après authentification
@app.get('/previsions/')
async def previsions_page(current_user: Annotated[str, Depends(get_current_active_user)]):
    return {'page prévision'}

@app.get('/dashboard/')
async def dashboard_page(current_user: Annotated[str, Depends(get_current_active_user)]):
    if current_user.scope == 'admin':
        return 'page autorisé'
    else:
        raise HTTPException(status_code = 401, detail = 'Unauthorized')
