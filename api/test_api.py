from fastapi.testclient import TestClient

from .main import app
import bcrypt

client = TestClient(app)


###### test des enpoints

def test_home_page():
    response = client.get('/')
    assert response.status_code == 200


def test_prevision():
    response = client.get('/previsions/')
    assert response.status_code == 401


def test_login():
    response = client.post('/login', data= {'username' : 'user1', 'password' : 'password1'})
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

    response = client.post('/login', data = {'username' : 'wrong_username', 'password' : 'wrong_password'})
    assert response.status_code == 401

    response = client.post('/login', data = {'username' :'user1', 'password' : 'wrong_password'})
    assert response.status_code == 401

    response = client.post('/login', data = {'username' :'user3', 'password' : 'password3'})
    assert response.status_code == 401


def test_me():
    response = client.get('/users/me')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'

    response = client.post('/login', data = {'username' : 'user1', 'password' : 'password1'})
    assert 'access_token' in response.json()

    token = response.json()['access_token']

    response = client.get('/users/me', headers = {'Authorization' : f'Bearer {token}'})
    assert response.json()['username'] == 'user1'



def test_dashboard():
    response = client.get('/dashboard')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'

    response = client.post('/login', data = {'username' : 'user1', 'password' : 'password1'})
    token = response.json()['access_token']
    response = client.get('/dashboard', headers = {'Authorization' : f'Bearer {token}'})
    assert response.status_code == 401

    response = client.post('/login', data = {'username' : 'user2', 'password' : 'password2'})
    token = response.json()['access_token']
    response = client.get('/dashboard', headers = {'Authorization' : f'Bearer {token}'})
    assert response.status_code == 200


### test fonction

def test_hashage():
    password = bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt())
    assert bcrypt.checkpw('password1'.encode('utf-8'), password)
