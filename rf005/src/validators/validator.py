from src.errors.errors import TokenNoEnviado, TokenVencido, ErrorUUID
from src.utils.utils import FileUtils
import uuid


class ValidadorConsultas():

    def validar_consulta(self, headers, token, postId):
        token_encabezado = token
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        
        return True
        
    def validar_token_enviado(self, token):
        if token is None:
            raise TokenNoEnviado
    
    def validar_token_vencido(self, token):
        parts_token = token.split()
        if "fake" in parts_token[1]:
            raise TokenVencido
