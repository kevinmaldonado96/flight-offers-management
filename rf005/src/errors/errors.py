class ApiError(Exception):
    code = 422
    description = "Default message"

class TokenNoEnviado(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class PostNoAutorizado(ApiError):
    code = 403
    description = "El usuario no tiene permiso para ver el contenido de esta publicación"

class TokenVencido(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class CamposFaltantes(ApiError):
    code = 400
    description = "Los campos de la petición están incompletos o no cumplen el formato esperado"

class PostNoExiste(ApiError):
    code = 404
    description = "El post no existe"

class ErrorUUID(ApiError):
    code = 400
    description = "El id no es un valor string con formato uuid."

class TrayectoNoExiste(ApiError):
    code = 404
    description = "El trayecto no existe"

class OfertaNoExiste(ApiError):
    code = 404
    description = "La oferta no existe"

class ErrorServicio(ApiError):
    code = 500
    description = "Error al consumir el servicio."