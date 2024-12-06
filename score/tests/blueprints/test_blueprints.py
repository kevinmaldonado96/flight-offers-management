from datetime import datetime, timedelta

import json
from src.main import app
import pytest
import random
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


class TestScores:
    def test_health(self):
        with app.test_client() as test_client:
            response = test_client.get('/scores/ping')

            assert response.status_code == 200
            assert response.data == b'pong'

    def test_status_code_calculate(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('src.commands.create.Create.get_user_id', return_value='1234567890')
            data = self.get_calculate_data()
            response_service = test_client.post('/scores/calculate', json=data, headers={'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"})
            assert response_service.status_code == 201

    def test_calculate_score(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.create.requests.get',
                         return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('src.commands.create.Create.get_user_id', return_value='1234567890')
            data = self.get_calculate_data()
            response_service = test_client.post('/scores/calculate', json=data, headers={'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"})
            value = json.loads(response_service.data).get('value')
            assert value == self.calculate_score(data=data)

    @staticmethod
    def calculate_score(data):

        if data.get('size') == 'SMALL':
            size = 0.25
        elif data.get('size') == 'MEDIUM':
            size = 0.5
        else:
            size = 1

        value = (float(data.get("offer")) - ((float(size) * float(data.get('bagCost')))))

        return value

    @staticmethod
    def get_calculate_data():
        return {
            "size": random.choice(["SMALL", "MEDIUM"]),
            "offer": str(fake.random_int()),
            "bagCost": str(fake.random_int())
        }

    @staticmethod
    def request_scores_data():
        created_date = (datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        data = {
            'value': str(fake.random_int()),
            'createdAt': created_date,
        }

        return data

