from datetime import datetime, timedelta, timezone

import sqlite3
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated, Union, Literal, Optional
from pydantic import BaseModel, EmailStr
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

import json

SECRET_KEY = '94229c6c19e9ae7adebf61f8e7565d1990727ce8f13b8f11bf1aa3e481a94947'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


load_dotenv()
db_url = os.getenv('DB_PATH')


class User(BaseModel):
    username : str
    email : EmailStr
    scope : Literal['user', 'admin'] = 'user'
    disabled : Union[bool, None] = None



class UserInDB(User):
    hashed_password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Union[str , None] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login',
                                     description = 'token pour authentifier l\'user lors de la conexion')



app = FastAPI()


def get_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_user(username: str):
    con = sqlite3.connect(f'{db_url}')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        res = cur.execute("""SELECT username, email, scope, password as hashed_password
                          FROM users
                          WHERE username = ?""",
                          (username,))
        user = res.fetchone()
    except sqlite3.IntegrityError:
        return 'pas trouvé'
    con.close()
    if user:
        return UserInDB(**dict(user))
    return None

def authenticate_user(username : str, password : str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data : dict, expires_delta : Union[timedelta , None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers = {'WWW-authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user : Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code = 400, detail = 'Inactive user')
    return current_user


@app.get('/')
async def welcome_page(current_user: Annotated[Optional[User], Depends(get_current_user)]):
    if current_user:
        return {'message' : f'Welcome to Meteostralia from API {current_user.username}',
                'current_user' : current_user}
    # else:
    #     return{'message' : 'Welcome to Meteostralia from API disconnected'}


@app.post('/login')
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm,
                                                 Depends()],) -> Token:
    user = authenticate_user(data.username, data.password)
    if not user or user.disabled:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Incorrect username or password or email',
                            headers={'WWW-Authenticate': 'Bearer'})

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {'sub' : user.username},
                                       expires_delta = access_token_expires)

    return Token(access_token = access_token, token_type = 'bearer')

@app.post('/sign_up')
async def register_user(data : UserInDB):
    username = data.username
    hashed_password = get_hash(data.hashed_password)
    email = data.email
    scope = 'user'

    con = sqlite3.connect(f'{db_url}')
    cur = con.cursor()

    try:
        cur.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")

        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        existing_username = cur.fetchone()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already in use")

        cur.execute("""INSERT INTO users(username, email, password, scope)
                        VALUES(?, ?, ?, ?)""",
                        (username, email, hashed_password, scope))
        con.commit()
    finally:
        con.close()

    return {'message': 'User created successfully'}

@app.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user:
        return current_user
    else:
        return HTTPException(status_code = 401, detail = 'Unauthorized')

@app.get('/previsions/')
async def previsions_page(current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user:
        return current_user
    else:
        return HTTPException(status_code = 401, detail = 'Unauthorized')

@app.get('/dashboard/')
async def dashboard_page(current_user: Annotated[str, Depends(get_current_active_user)]):
    print(current_user)
    if current_user.scope == 'admin':
        return 'page autorisé'
    else:
        raise HTTPException(status_code = 401, detail = 'Unauthorized')
