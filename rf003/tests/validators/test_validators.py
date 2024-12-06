import pytest
from faker import Faker
from src.main import app
from datetime import datetime, timedelta
from src.validators.validators import Validador
from src.errors.errors import Rf003Exception

fake = Faker()
validador = Validador()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    
class TestBlueprints():
    
    def test_validador_datos_faltantes(self):
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

        with pytest.raises(Rf003Exception):
            validador.validar_creacion_publicacion({"flightId": fake.name()}, headers)

    def test_validador_sin_header(self):
        headers = {'Authorization': ""}

        with pytest.raises(Rf003Exception):
            validador.validar_creacion_publicacion({"flightId": fake.name()}, headers)

    def test_validador_sin_header(self):
        headers = {'Authorization': ""}

        with pytest.raises(Rf003Exception):
            validador.validar_creacion_publicacion({"flightId": fake.name()}, headers)

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