
import json
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

    def test_campos_invalidos_creacion_trayecto(self, mocker):
        with app.test_client() as test_client:
            
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = {'flightId': fake.name()}
            response_service = test_client.post('/routes/',json=data, headers=headers)

            print(response_service)

            assert response_service.status_code == 400

    def test_campos_creacion_start_date_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            end_date= self.generar_fecha()
            end_date_iso = self.generar_fecha_formato_iso8601(end_date)

            data = {
                'flightId': fake.name(),
                'sourceAirportCode': fake.name(),
                'sourceCountry': fake.name(),
                'destinyAirportCode': fake.name(),
                'destinyCountry': fake.name(),
                'bagCost': fake.name(),
                'plannedStartDate': '2022-08-01T21:20:53.214Z',
                'plannedEndDate': end_date_iso}
            
            response_service = test_client.post('/routes/',json=data, headers=headers)

            assert response_service.status_code == 412

    def test_campos_creacion_end_date_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            start_date= self.generar_fecha()
            start_date_iso = self.generar_fecha_formato_iso8601(start_date)

            data = {
                'flightId': fake.name(),
                'sourceAirportCode': fake.name(),
                'sourceCountry': fake.name(),
                'destinyAirportCode': fake.name(),
                'destinyCountry': fake.name(),
                'bagCost': fake.name(),
                'plannedStartDate': start_date_iso,
                'plannedEndDate': '2022-08-01T21:20:53.214Z'}
            
            response_service = test_client.post('/routes/',json=data, headers=headers)

            assert response_service.status_code == 412

    def test_campos_creacion_start_end_fechas_solapadas(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            end_date= self.generar_fecha()
            end_date_iso = self.generar_fecha_formato_iso8601(end_date)

            start_date = end_date + timedelta(days=5)
            start_date_iso = self.generar_fecha_formato_iso8601(start_date)


            data = {
                'flightId': fake.name(),
                'sourceAirportCode': fake.name(),
                'sourceCountry': fake.name(),
                'destinyAirportCode': fake.name(),
                'destinyCountry': fake.name(),
                'bagCost': fake.name(),
                'plannedStartDate': start_date_iso,
                'plannedEndDate': end_date_iso}
            
            response_service = test_client.post('/routes/',json=data, headers=headers)

            assert response_service.status_code == 412

    def test_creacion_sin_token(self):
        with app.test_client() as test_client:
            data = self.request_trayecto_exitoso_data()
            
            response_service = test_client.post('/routes/',json=data)
     
            assert response_service.status_code == 403

    def test_creacion_token_invalido(self, mocker, client):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
            data = self.request_trayecto_exitoso_data()
            
            response_service = test_client.post('/routes/',json=data, headers=headers)
     
            assert response_service.status_code == 401

    def test_creacion_trayecto(self, mocker, client):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.request_trayecto_exitoso_data()
            
            response_service = test_client.post('/routes/',json=data, headers=headers)
     
            assert response_service.status_code == 201

    
    def test_creacion_trayecto_flighid_existente(self, mocker, client):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.request_trayecto_exitoso_data()
            
            test_client.post('/routes/',json=data, headers=headers)
            response_service_repetido = test_client.post('/routes/',json=data, headers=headers)
     
            assert response_service_repetido.status_code == 412

    def test_consulta_trayectos_sin_filtro(self, mocker, client):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.request_trayecto_exitoso_data()            
            test_client.post('/routes/',json=data, headers=headers)

            data = self.request_trayecto_exitoso_data()  
            test_client.post('/routes/',json=data, headers=headers)
     
            trayectos = test_client.get('/routes/', headers=headers)
            trayectos_data = json.loads(trayectos.data)

            assert trayectos.status_code == 200
            assert len(trayectos_data) > 1

    def test_consulta_trayectos_sin_token(self):
        with app.test_client() as test_client:
     
            trayectos = test_client.get('/routes/')
            assert trayectos.status_code == 403

    def test_consulta_trayectos_token_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            trayectos = test_client.get('/routes/', headers=headers)

            assert trayectos.status_code == 401

    def test_consulta_trayectos_token_filtrar_flightid(self, mocker):
        with app.test_client() as test_client:
            
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            test_client.post('/routes/',json=data, headers=headers)

            trayectos = test_client.get(f"/routes/?flight={data['flightId']}", headers=headers)
            trayectos_data = json.loads(trayectos.data)

            assert trayectos.status_code == 200
            assert trayectos_data[0].get("flightId") == data.get("flightId")

    def test_consulta_trayectos_token_filtrar_flightid_no_existe(self, mocker):
        with app.test_client() as test_client:
            
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            test_client.post('/routes/',json=data, headers=headers)

            trayectos = test_client.get(f"/routes/?flight=fake", headers=headers)
            trayectos_data = json.loads(trayectos.data)

            assert trayectos.status_code == 200
            assert len(trayectos_data) == 0

    def test_consulta_trayecto_por_id_sin_token(self):
        with app.test_client() as test_client:
     
            trayectos = test_client.get('/routes/fake')
            assert trayectos.status_code == 403

    def test_consulta_trayecto_por_id_token_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            trayectos = test_client.get('/routes/fake', headers=headers)

            data = self.request_trayecto_exitoso_data()            
            test_client.post('/routes/',json=data, headers=headers)

            assert trayectos.status_code == 401

    def test_consulta_trayecto_por_id_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            trayectos = test_client.get('/routes/fake', headers=headers)

            assert trayectos.status_code == 400

    def test_consulta_trayecto_exitoso(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            response_post = test_client.post('/routes/',json=data, headers=headers)
            response_post_data = json.loads(response_post.data)

            trayectos = test_client.get(f"/routes/{response_post_data['id']}", headers=headers)
            trayectos_data = json.loads(trayectos.data)

            assert trayectos.status_code == 200
            assert trayectos_data['id'] == response_post_data['id']

    def test_consulta_trayecto_por_id_no_existe(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            response_post = test_client.post('/routes/',json=data, headers=headers)
            response_post_data = json.loads(response_post.data)

            test_client.delete(f"/routes/{response_post_data['id']}", headers=headers)

            trayectos = test_client.get(f"/routes/{response_post_data['id']}", headers=headers)

            assert trayectos.status_code == 404
        
    def test_eliminar_trayectos_sin_token(self):
        with app.test_client() as test_client:
     
            trayectos = test_client.delete('/routes/fake')
            assert trayectos.status_code == 403

    def test_eliminar_trayectos_token_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            trayectos = test_client.delete('/routes/fake', headers=headers)

            assert trayectos.status_code == 401

    def test_eliminar_trayecto_por_id_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            trayectos = test_client.get('/routes/fake', headers=headers)

            assert trayectos.status_code == 400
    
    def test_eliminar_trayecto_exitoso(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            response_post = test_client.post('/routes/',json=data, headers=headers)
            response_post_data = json.loads(response_post.data)

            trayectos = test_client.delete(f"/routes/{response_post_data['id']}", headers=headers)

            assert trayectos.status_code == 200

    def test_eliminar_trayecto_id_no_existe(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            data = self.request_trayecto_exitoso_data()            
            response_post = test_client.post('/routes/',json=data, headers=headers)
            response_post_data = json.loads(response_post.data)


            test_client.delete(f"/routes/{response_post_data['id']}", headers=headers)
            trayectos = test_client.delete(f"/routes/{response_post_data['id']}", headers=headers)

            assert trayectos.status_code == 404

    def request_trayecto_exitoso_data(self):
        
            start_date= self.generar_fecha()
            start_date_iso = self.generar_fecha_formato_iso8601(start_date)

            end_date = start_date + timedelta(days=5)
            end_date_iso = self.generar_fecha_formato_iso8601(end_date)

            data = {
                'flightId': fake.name(),
                'sourceAirportCode': fake.name(),
                'sourceCountry': fake.name(),
                'destinyAirportCode': fake.name(),
                'destinyCountry': fake.name(),
                'bagCost': fake.random_int(min=1, max=100),
                'plannedStartDate': start_date_iso,
                'plannedEndDate': end_date_iso}
            
            return data

    def generar_fecha(self):

        today = datetime.now()
        random_datetime = fake.date_time_between_dates(datetime_start=today+timedelta(days=1), datetime_end=today + timedelta(days=365))
        return random_datetime
    
    def generar_fecha_formato_iso8601(self, fecha_random):
        iso8601_with_milliseconds = fecha_random.isoformat(timespec='milliseconds') + 'Z'
        return iso8601_with_milliseconds
 



