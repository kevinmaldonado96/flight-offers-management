import json
import pytest
import unittest
import requests
from src.main import app
from faker import Faker
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from src.validators.validator import ValidadorConsultas, TokenVencido
from src.commands.get_post import GetPost, PostNoExiste
from src.errors.errors import CamposFaltantes, TrayectoNoExiste, OfertaNoExiste, ErrorServicio
from src.utils.utils import FileUtils


fake = Faker()
headers = {"Authorization": "Bearer 123456"}

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    
class TestGetPost(unittest.TestCase):

    def setUp(self):
        self.validator = ValidadorConsultas()

    def test_validar_token_vencido_raise_exception(self):
        token = "Bearer fake_token"
        with self.assertRaises(TokenVencido):
            self.validator.validar_token_vencido(token)
    
    def test_sin_token(self):
        with app.test_client() as test_client:
            response = test_client.get('rf005/posts/15')

            assert response.status_code == 403
    
    @staticmethod
    def test_get_post():
        postId = "some_post_id"
        token = "some_token"
        headers = {'Authorization': token}
        response_data = {'id': postId, 'title': 'Some title'}

        with patch('src.commands.get_post.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = response_data

            get_post_command = GetPost(postId, headers, token)
            result = get_post_command.get_post(postId)

            assert result == response_data
    
    @staticmethod
    def test_get_post_missing_post_id():
        # Definir datos de prueba
        postId = None
        token = "some_token"
        headers = {'Authorization': token}

        # Crear una instancia de GetPost
        get_post_command = GetPost(postId, headers, token)

        # Verificar que se levante una excepción CamposFaltantes
        with pytest.raises(CamposFaltantes):
            get_post_command.get_post(postId)

    @staticmethod
    def test_get_post_not_found():
        # Definir datos de prueba
        postId = "non_existing_post_id"
        token = "some_token"
        headers = {'Authorization': token}

        # Configurar el parche para requests.get
        with patch('src.commands.get_post.requests.get') as mock_get:
            # Configurar el comportamiento simulado de requests.get
            mock_get.return_value.status_code = 404

            # Crear una instancia de GetPost
            get_post_command = GetPost(postId, headers, token)

            # Verificar que se levante una excepción PostNoExiste
            with pytest.raises(PostNoExiste):
                get_post_command.get_post(postId)
    
    @patch('src.commands.get_post.requests.get')
    def test_get_route_success(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'route_id',
            'flightId': 'flight_id',
            'sourceAirportCode': 'source_airport_code',
            'sourceCountry': 'source_country',
            'destinyAirportCode': 'destiny_airport_code',
            'destinyCountry': 'destiny_country',
            'bagCost': 100
        }

        # Configurar los argumentos de la función
        route_id = 'route_id'
        headers = {'Authorization': 'Bearer token'}
        token = 'token'

        # Crear una instancia de GetPost
        get_post_command = GetPost(None, headers, token)

        # Llamar a la función get_route
        route_data = get_post_command.get_route(route_id)

        # Verificar que la función devuelva los datos de la ruta
        self.assertEqual(route_data['id'], 'route_id')
        self.assertEqual(route_data['flightId'], 'flight_id')
        self.assertEqual(route_data['sourceAirportCode'], 'source_airport_code')
        self.assertEqual(route_data['sourceCountry'], 'source_country')
        self.assertEqual(route_data['destinyAirportCode'], 'destiny_airport_code')
        self.assertEqual(route_data['destinyCountry'], 'destiny_country')
        self.assertEqual(route_data['bagCost'], 100)

    @patch('src.commands.get_post.requests.get')
    def test_get_route_failure(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # Configurar los argumentos de la función
        route_id = 'non_existing_route_id'
        headers = {'Authorization': 'Bearer token'}
        token = 'token'

        # Crear una instancia de GetPost
        get_post_command = GetPost(None, headers, token)

        # Verificar que la función levante una excepción TrayectoNoExiste
        with self.assertRaises(TrayectoNoExiste):
            get_post_command.get_route(route_id)

    @patch('src.commands.get_post.requests.get')
    def test_get_offer_success(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 'offer_id', 'userId': 'user_id'}]

        # Configurar los argumentos de la función
        post_id = 'post_id'
        headers = {'Authorization': 'Bearer token'}
        token = 'token'

        # Crear una instancia de GetPost
        get_post_command = GetPost(None, headers, token)

        # Llamar a la función get_offer
        offer_data = get_post_command.get_offer(post_id)

        # Verificar que la función devuelva los datos de la oferta
        self.assertEqual(len(offer_data), 1)
        self.assertEqual(offer_data[0]['id'], 'offer_id')
        self.assertEqual(offer_data[0]['userId'], 'user_id')

    @patch('src.commands.get_post.requests.get')
    def test_get_offer_failure(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # Configurar los argumentos de la función
        post_id = 'non_existing_post_id'
        headers = {'Authorization': 'Bearer token'}
        token = 'token'

        # Crear una instancia de GetPost
        get_post_command = GetPost(None, headers, token)

        # Verificar que la función levante una excepción OfertaNoExiste
        with self.assertRaises(OfertaNoExiste):
            get_post_command.get_offer(post_id)

    @patch('src.utils.utils.requests.get')
    def test_get_user_success(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'user_id'}

        # Configurar los argumentos de la función
        headers = {'Authorization': 'Bearer some_token'}

        # Llamar a la función get_user
        file_utils = FileUtils()
        user_id = file_utils.get_user(headers)

        # Verificar que la función devuelva el ID de usuario esperado
        self.assertEqual(user_id, 'user_id')

    @patch('src.utils.utils.requests.get')
    def test_get_user_token_expired(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 401

        # Configurar los argumentos de la función
        headers = {'Authorization': 'Bearer expired_token'}

        # Llamar a la función get_user
        file_utils = FileUtils()

        # Verificar que la función levante una excepción TokenVencido
        with self.assertRaises(TokenVencido):
            file_utils.get_user(headers)

    @patch('src.utils.utils.requests.get')
    def test_get_user_service_error(self, mock_get):
        # Configurar el comportamiento simulado de requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        # Configurar los argumentos de la función
        headers = {'Authorization': 'Bearer some_token'}

        # Llamar a la función get_user
        file_utils = FileUtils()

        # Verificar que la función levante una excepción ErrorServicio
        with self.assertRaises(ErrorServicio):
            file_utils.get_user(headers)
