from datetime import datetime, timedelta

import json
from src.main import app
import pytest
from faker import Faker

fake = Faker()
headers = {"Authorization": "Bearer 123456"}
SIZES = ["LARGE", "MEDIUM", "SMALL"]

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_ok_authorization(mocker):
    mock = mocker.patch('requests.get')
    mock.return_value.status_code = 200
    return mock


class TestPosts:
    def test_health(self):
        with app.test_client() as test_client:
            response = test_client.get('/posts/ping')

            assert response.status_code == 200
            assert response.data == b'pong'

    def test_without_token(self):
        with app.test_client() as test_client:
            response = test_client.post('/posts/', json={})

            assert response.status_code == 403

    def test_crete_post(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('src.commands.create.Create.get_user_id', return_value='1234567890')
            data = self.request_posts_data()
            print(data)
            response_service = test_client.post('/posts/', json=data, headers={'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"})

            assert response_service.status_code == 201

    def test_create_failed_post(self, mock_ok_authorization):
        with app.test_client() as test_client:
            headers = {"Authorization": "Bearer 123456"}
            data = self.request_posts_data()
            data['expireAt'] = (datetime.now() + timedelta(days=-2)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            response = test_client.post('/posts/', json=data, headers=headers)

            assert response.status_code == 412

    def test_create_data_failed_post(self, mock_ok_authorization):
        with app.test_client() as test_client:
            headers = {"Authorization": "Bearer 123456"}
            data = self.request_posts_data()
            del data['routeId']
            response = test_client.post('/posts/', json=data, headers=headers)
            assert response.status_code == 400

    def test_list_posts(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            response_service = test_client.get('/posts/', headers={'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"})

            assert response_service.status_code == 200


    def test_list_posts_all_filters(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            response_service = test_client.get('/posts/', headers={'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"})

            assert response_service.status_code == 200

    def test_not_found_posts_id(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            posts = test_client.get(f"/routes/?post_id=0bbcb410-4263-49fd-a553-62e98eabd7e3", headers=headers)

            assert posts.status_code == 404

    def test_without_token_posts_id(self):
        with app.test_client() as test_client:
            response = test_client.get('/posts/abc')

            assert response.status_code == 403



    @staticmethod
    def request_posts_data():
        expire_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        data = {
            'routeId': str(fake.random_int()),
            'userId': str(fake.random_int()),
            'expireAt': expire_date,
        }

        return data

