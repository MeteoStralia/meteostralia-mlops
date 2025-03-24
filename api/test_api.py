import os
import sqlite3
from fastapi.testclient import TestClient
from .main import app
import bcrypt

client = TestClient(app)

def create_test_db():
    con = sqlite3.connect('../test_database.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            email TEXT,
            scope TEXT,
            password TEXT
        )
    ''')

    cur.execute('''
        INSERT OR IGNORE INTO users (username, email, scope, password)
        VALUES
        ('user1', 'user1@example.com', 'user', ?),
        ('user2', 'user2@example.com', 'user', ?),
        ('admin', 'admin@example.com', 'admin', ?)
    ''', (
        bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    ))
    con.commit()
    con.close()

def setup_module(module):
    create_test_db()

def teardown_module(module):
    if os.path.exists('../test_database.db'):
        os.remove('../test_database.db')
        print("Test database removed.")


# def test_home_page():
#     response = client.get('/')
#     assert response.status_code == 401

#     response = client.post('/login', data={'username': 'user2', 'password': 'password2'})
#     assert response.status_code == 200
#     token = response.json()['access_token']

#     response = client.get('/', headers={'Authorization': f'Bearer {token}'})
#     assert response.status_code == 200

# def test_signup():

    # username = 'newuser'
    # hashed_password = get_hash('newpassword')
    # email = data.email
    # scope = 'user'

    # response = client.post('/signup', data={'username': 'newuser', 'email': 'newuser@mail.com', 'password': 'newpassword'})
    # assert response.status_code == 201
    # assert response.json()['message'] == 'User created successfully'

    # con = sqlite3.connect('../test_database.db')
    # cur = con.cursor()
    # res = cur.execute("SELECT username FROM users WHERE username = 'newuser'")
    # user = res.fetchone()
    # assert user is not None
    # con.close()

    # response = client.post('/signup', json={'username': 'user1', 'password': 'password1'})
    # assert response.status_code == 400
    # assert response.json()['detail'] == 'Username already taken'

    # # Test signup with weak password (e.g., too short)
    # response = client.post('/signup', json={'username': 'weakuser', 'password': 'short'})
    # assert response.status_code == 400
    # assert response.json()['detail'] == 'Password is too short'

def test_prevision():
    response = client.get('/previsions/')
    assert response.status_code == 401

# def test_login():
#     response = client.post('/login', data={'username': 'user1', 'password': 'password1'})
#     assert response.status_code == 200
#     assert 'access_token' in response.json()
#     assert response.json()['token_type'] == 'bearer'

#     response = client.post('/login', data={'username': 'wrong_username', 'password': 'wrong_password'})
#     assert response.status_code == 401

#     response = client.post('/login', data={'username': 'user1', 'password': 'wrong_password'})
#     assert response.status_code == 401

#     response = client.post('/login', data={'username': 'user3', 'password': 'password333'})
#     assert response.status_code == 401

# def test_me():
#     response = client.get('/users/me')
#     assert response.status_code == 401
#     assert response.json()['detail'] == 'Not authenticated'

#     response = client.post('/login', data={'username': 'user1', 'password': 'password1'})
#     assert 'access_token' in response.json()
#     token = response.json()['access_token']

#     response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
#     assert response.json()['username'] == 'user1'

# def test_dashboard():
#     response = client.get('/dashboard')
#     assert response.status_code == 401
#     assert response.json()['detail'] == 'Not authenticated'

#     response = client.post('/login', data={'username': 'user1', 'password': 'password1'})
#     token = response.json()['access_token']
#     response = client.get('/dashboard', headers={'Authorization': f'Bearer {token}'})
#     assert response.status_code == 401

#     response = client.post('/login', data={'username': 'admin', 'password': 'admin'})
#     token = response.json()['access_token']
#     response = client.get('/dashboard', headers={'Authorization': f'Bearer {token}'})
#     assert response.status_code == 200

def test_hashage():
    password = bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt())
    assert bcrypt.checkpw('password1'.encode('utf-8'), password)
