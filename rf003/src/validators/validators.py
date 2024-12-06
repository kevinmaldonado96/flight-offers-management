from ..errors.errors import Rf003Exception
from datetime import datetime

campos_requeridos = ['flightId', 'expireAt', 'plannedStartDate', 'plannedEndDate', 'origin', 'destiny', 'bagCost']

class Validador():

    def validar_creacion_publicacion(self, data, headers):
         
        token_encabezado = headers.get('Authorization')

        self.validar_token_enviado(token_encabezado)
        self.validar_campos(data)
        self.validate_date_expireAt(data)
    
    def validar_token_enviado(self, token):
        if token is None:
            raise Rf003Exception(403, F"El token no se encuentra en la solicitud")
    
    def validar_campos(self, data):
          
        for campo in campos_requeridos:
            if campo not in data:
                raise Rf003Exception(400, F"Falta el campo {campo} en la petició enviada")

        if "airportCode" not in data["origin"] or "country" not in data["origin"]:
               raise Rf003Exception(400, F"Falta el campo airportCode o el campo country en origin")
    
        if "airportCode" not in data["destiny"] or "country" not in data["destiny"]:
               raise Rf003Exception(400, F"Falta el campo airportCode o el campo country en destiny")

    def validate_date_expireAt(self, data):
        raw_date = datetime.strptime(data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ")
        now_iso_format = datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ")
        validated_date = bool(datetime.strptime(data.get("expireAt"), "%Y-%m-%dT%H:%M:%S.%fZ"))

        if raw_date > now_iso_format and validated_date:
            return True
        else:
            raise Rf003Exception(412, F"La fecha expiración no es válida")
