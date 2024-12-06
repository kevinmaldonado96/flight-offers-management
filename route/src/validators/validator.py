from datetime import datetime
from ..errors.errors import Fechasinvalidas, TokenNoEnviado, TokenInvalido, FlightIdExistente, ErrorServicio, CamposFaltantes, IdFormatoInvalido, RegistroIdNoExiste
from ..commands.trayecto_command import TrayectoCommand
import uuid
import logging
import requests

campos_requeridos = ['flightId', 'sourceAirportCode', 'sourceCountry', 'destinyAirportCode', 'destinyCountry', 'bagCost', 'plannedStartDate', 'plannedEndDate']

class ValidadorTrayectos():

    def validar_request_creacion(self, data, headers):

        # validacion de token
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_valido(token_encabezado)

        # validacion campos requeridos
        self.validar_campos_requeridos(data)

        # validacion de fechas
        fecha_start_parseada = self.validar_formato_fecha_start_date(data.get('plannedStartDate'))
        self.validar_fecha_no_mayor_actual(fecha_start_parseada)

        fecha_end_parseada = self.validar_formato_fecha_start_date(data.get('plannedEndDate'))
        self.validar_fecha_no_mayor_actual(fecha_end_parseada)

        self.validar_fecha_start_menor_fecha_end(fecha_start_parseada, fecha_end_parseada)

        ## validacion flightIdExistente
        self.validar_flightId_repetido(data.get('flightId'))

        return True
    
    def validar_consulta_flight(self, headers):
        # validacion de token
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_valido(token_encabezado) 

        return True
    
    def validar_consulta_por_id(self, id, headers):

          # validacion de token
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado) 
        self.validar_token_valido(token_encabezado)

        #validar formato id
        self.validar_id_uuid(id)

        return True
    
    def validar_eliminar_por_id(self, id, headers):

        # validacion de token
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado) 
        self.validar_token_valido(token_encabezado)

        #validar formato id
        self.validar_id_uuid(id)

        #validar formato id
        self.validar_id_existente(id)

        return True
    

    def validar_fecha_no_mayor_actual(self, fecha):
        fecha_actual = datetime.now()
        if fecha < fecha_actual:
            raise Fechasinvalidas

    
    def validar_formato_fecha_start_date(self, fecha_request):
        try:
            fecha_parseada = datetime.strptime(fecha_request, '%Y-%m-%dT%H:%M:%S.%fZ')
            return fecha_parseada
        except ValueError:
            raise Fechasinvalidas

    def validar_fecha_start_menor_fecha_end(self, fecha_start, fecha_end):
        if fecha_end < fecha_start:
            raise Fechasinvalidas
        
    def validar_token_enviado(self, token):
        if token is None:
            raise TokenNoEnviado
        
    def validar_id_existente(self, id):
        trayecto = TrayectoCommand().consultar_trayecto_por_id(id)
        if trayecto is None:
            raise RegistroIdNoExiste
        
    def validar_flightId_repetido(self, flightId):
        trayectos = TrayectoCommand().consultar_trayecto_por_flightId(flightId)
        logging.debug(trayectos)
        if trayectos is not None and trayectos :
            raise FlightIdExistente
        
    def validar_campos_requeridos(self, data):
        for campo in campos_requeridos:
            if campo not in data:
                raise CamposFaltantes
 
        
    def validar_id_uuid(self, id):
        try:
            uuid_obj = uuid.UUID(id, version=4)
            return True
        except ValueError:
            raise IdFormatoInvalido
        
    def validar_token_valido(self, token):
            token_sin_bearer = token[len('Bearer '):]
            logging.debug(f"token sin bearer {token_sin_bearer}")

            url = 'http://users:3000/user/me'

            headers = {
                "Authorization": f"Bearer {token_sin_bearer}",
                      }

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                raise TokenInvalido
            else:
                raise ErrorServicio

