import json
import pytest
from faker import Faker
from src.validators.validator import ValidadorTrayectos
from src.errors.errors import CamposFaltantes, Fechasinvalidas, RegistroIdNoExiste, TokenNoEnviado, TokenInvalido, IdFormatoInvalido
from src.models.models import db
from datetime import datetime, timedelta

fake = Faker()
validador = ValidadorTrayectos()

class TestValidation():
    def test_validacion_campos_invalidos_creacion_trayecto(self, mocker):
        mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
        
        data = {'flightId': fake.name()}
        with pytest.raises(CamposFaltantes):
          validador.validar_request_creacion(data, headers)


    def test_validador_campos_creacion_start_date_invalido(self, mocker):

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
            
            with pytest.raises(Fechasinvalidas):
                validador.validar_request_creacion(data, headers)

    def test_validador_campos_creacion_end_date_invalido(self, mocker):

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
            
            with pytest.raises(Fechasinvalidas):
                validador.validar_request_creacion(data, headers)

    def test_validador_campos_creacion_start_end_fechas_solapadas(self, mocker):

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
               
            with pytest.raises(Fechasinvalidas):
                validador.validar_request_creacion(data, headers)

    def test_validador_creacion_sin_token(self):
            headers = {}
            data = {}    
        
            with pytest.raises(TokenNoEnviado):
                validador.validar_request_creacion(data, headers)  

    def test_validador_creacion_token_invalido(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
            data = self.request_trayecto_exitoso_data()
            
            with pytest.raises(TokenInvalido):
                validador.validar_request_creacion(data, headers)   

    def test_validador_creacion_trayecto(self, mocker):
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            data = self.request_trayecto_exitoso_data()
            response = validador.validar_request_creacion(data, headers)          
    
            assert response == True

    def test_validador_consulta_trayectos_sin_filtro(self, mocker):

            headers = {}
            with pytest.raises(TokenNoEnviado):
                validador.validar_consulta_flight(headers)

    def test_consulta_trayectos_token_invalido(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            with pytest.raises(TokenInvalido):
                validador.validar_consulta_flight(headers)

    def test_creacion_trayecto_flighid_existente(self, mocker):
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            response = validador.validar_consulta_flight(headers)
            assert response == True

    
    def test_consulta_validacion_trayecto_por_id_sin_token(self):       
            headers = {}
            with pytest.raises(TokenNoEnviado):
                validador.validar_consulta_por_id('fake',headers)

    def test_validacion_consulta_trayecto_por_id_token_invalido(self, mocker):
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            with pytest.raises(TokenInvalido):
                validador.validar_consulta_por_id('fake',headers)

    def test_validacion_consulta_trayecto_por_id_invalido(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            with pytest.raises(IdFormatoInvalido):
                validador.validar_consulta_por_id('fake',headers)

    def test_validacion_consulta_trayecto_id_no_existe(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            response = validador.validar_consulta_por_id('0bbcb410-4263-49fd-a553-62e98eabd7e3',headers)
            assert response == True
            
    def test_eliminar_validacion_trayecto_por_id_sin_token(self):       
            headers = {}
            with pytest.raises(TokenNoEnviado):
                validador.validar_eliminar_por_id('fake',headers)

    def test_validacion_eliminar_trayecto_por_id_token_invalido(self, mocker):
            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Acceso prohibido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            with pytest.raises(TokenInvalido):
                validador.validar_eliminar_por_id('fake',headers)

    def test_validacion_eliminar_trayecto_por_id_invalido(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            with pytest.raises(IdFormatoInvalido):
                validador.validar_eliminar_por_id('fake',headers)

    def test_validacion_eliminar_trayecto_no_existe(self, mocker):

            mocker.patch('src.validators.validator.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
     
            with pytest.raises(RegistroIdNoExiste):
                validador.validar_eliminar_por_id('0bbcb410-4263-49fd-a553-62e98eabd7e3',headers)
            

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