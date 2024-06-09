from fastapi.testclient import TestClient
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
import pytest

from main import app

client = TestClient(app=app)

# @pytest.mark.anyio
# async def test_read_main():
#     token = client.post('/login', OAuth2PasswordRequestForm(username='misha', password='misha'))

#     response = client.get("/get_solo_tasks")
#     assert response.status_code == 200
#     assert response.json() == {"data": "Hello, stranger"}



# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"data": "Hello, stranger"}


# @pytest.mark.anyio
# async def test_get_solo_tasks():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         res = await ac.post('/login', data={'username': 'misha', 'password':'misha'})
#         data = res.json().get("access_token")
#         res = await ac.get('/get_solo_tasks', headers={'Authorization': f'Bearer {data}'})
#     assert res.status_code == 200

# pytest -W ignore::DeprecationWarning -vv -s 


@pytest.mark.anyio
async def test_get_solo_tasks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/login', data={'username': 'misha', 'password':'misha'})
        data = res.json().get("access_token")
        res = await ac.get('/get_solo_tasks', headers={'Authorization': f'Bearer {data}'})
    assert res.status_code == 200


@pytest.mark.anyio
async def test_create_task_solo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/login', data={'username': 'misha', 'password':'misha'})
        token = res.json().get("access_token")
        res = await ac.post(
            '/create_task_solo', 
            json={
                "title": "string",
                "description": "string",
                "start_date": str(datetime.now()),
                "end_date": str(datetime.now()),
                "done": False
            },
              headers={'Authorization': f'Bearer {token}'}
        )
        assert res.status_code == 200


@pytest.mark.anyio
async def test_create_subtask():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/login', data={'username': 'misha', 'password':'misha'})
        token = res.json().get("access_token")
        res = await ac.post(
            '/create_subtask/32', 
            json={
                "title": "string", 
                "description": "string", 
                "done": False
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert res.status_code == 200