import pytest
from faker import Faker
from src.main import app
from datetime import datetime, timedelta

fake = Faker()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    
class TestBlueprints():
    
    def test_post_sin_trayecto(self, mocker):

        with app.test_client() as test_client:

            mocker.patch('src.commands.trayecto_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: [{"id": fake.name()}]))
            mocker.patch('src.commands.post_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: [{"id": fake.name()}]))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.obtener_request()

            response_service = test_client.post('/rf003/posts',json=data, headers=headers)

            print(response_service)
            assert response_service.status_code == 412

    def test_creacion_sin_token(self):

        with app.test_client() as test_client:
            response_service = test_client.post('/rf003/posts',json={"flightId": fake.name()})

            print(response_service)
            assert response_service.status_code == 403

    def test_creacion_post_faltan_datos(self):

        with app.test_client() as test_client:

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
            response_service = test_client.post('/rf003/posts',json={"flightId": fake.name()}, headers=headers)

            print(response_service)
            assert response_service.status_code == 400


    def test_creacion_post_exitoso(self, mocker):

        with app.test_client() as test_client:

            mocker.patch('src.commands.trayecto_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: []))
            mocker.patch('src.commands.crear_trayecto.GenericRestClient.post', return_value=mocker.Mock(status_code=201, json=lambda: {"id": fake.random_int(min=0, max=100)}))
            mocker.patch('src.commands.post_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: []))
            mocker.patch('src.commands.crear_post.GenericRestClient.post', return_value=mocker.Mock(status_code=201, json=lambda: {"id": fake.random_int(min=0, max=100), "userId": fake.random_int(min=0, max=100)}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.obtener_request()

            response_service = test_client.post('/rf003/posts',json=data, headers=headers)

            print(response_service)
            assert response_service.status_code == 201

    def obtener_request(self):

        start_date= self.generar_fecha()
        start_date_iso = self.generar_fecha_formato_iso8601(start_date)

        end_date = start_date + timedelta(days=5)
        end_date_iso = self.generar_fecha_formato_iso8601(end_date)

        return {
            "flightId": fake.name(),
            "expireAt": start_date_iso,
            "plannedStartDate": start_date_iso,
            "plannedEndDate": end_date_iso,
            "origin": {
                "airportCode": fake.name(),
                "country": fake.name()
            },
            "destiny": {
                "airportCode": fake.name(),
                "country": fake.name()
            },
            "bagCost": fake.random_int(min=1, max=100)
        }

    def generar_fecha(self):

        today = datetime.now()
        random_datetime = fake.date_time_between_dates(datetime_start=today+timedelta(days=1), datetime_end=today + timedelta(days=365))
        return random_datetime
    
    def generar_fecha_formato_iso8601(self, fecha_random):
        iso8601_with_milliseconds = fecha_random.isoformat(timespec='milliseconds') + 'Z'
        return iso8601_with_milliseconds



