import pytest
from faker import Faker
from src.main import app
from src.commands.crear_post import CrearPost
from src.commands.crear_trayecto import CrearTrayecto
from src.commands.eliminar_trayecto import EliminarTrayecto
from src.commands.post_existe import PostExiste
from src.commands.trayecto_existe import TrayectoExiste
from datetime import datetime, timedelta


#eliminar_trayecto = EliminarTrayecto()
#post_existe = PostExiste()

fake = Faker()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestCommands:

    def test_crear_post(self, mocker):

        mocker.patch('src.commands.trayecto_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: [{"id": fake.name()}]))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}


        flight_id = fake.name()
        trayecto_existe = TrayectoExiste(flight_id, headers)
        response= trayecto_existe.ejecutar()


        assert response is not None

    def test_crear_trayecto(self, mocker):

        mocker.patch('src.commands.crear_trayecto.GenericRestClient.post', return_value=mocker.Mock(status_code=201, json=lambda: {"id": fake.random_int(min=0, max=100)}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}


        data = self.obtener_request()
        crear_trayecto = CrearTrayecto(data, headers)
        response= crear_trayecto.ejecutar()

        assert response is not None

    def test_crear_post(self, mocker):

        mocker.patch('src.commands.crear_post.GenericRestClient.post', return_value=mocker.Mock(status_code=201, json=lambda: {"id": fake.random_int(min=0, max=100), "userId": fake.random_int(min=0, max=100)}))
        mocker.patch('src.commands.eliminar_trayecto.GenericRestClient.delete', return_value=mocker.Mock(status_code=200, json=lambda: {"id": fake.random_int(min=0, max=100), "userId": fake.random_int(min=0, max=100)}))

        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

        crear_post = CrearPost(fake.name(), True, fake.name(), headers)

        response= crear_post.ejecutar()

        assert response is not None

    
    def test_crear_post(self, mocker):

        mocker.patch('src.commands.post_existe.GenericRestClient.get', return_value=mocker.Mock(status_code=200, json=lambda: []))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

        post_existe = PostExiste(fake.name(), headers)

        response= post_existe.ejecutar()



        
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