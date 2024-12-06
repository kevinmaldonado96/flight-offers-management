class ApiError(Exception):
    code = 422
    description = "Default message"

class Fechasinvalidas(ApiError):
    code = 412
    description = "Las fechas del trayecto no son válidas"

class TokenNoEnviado(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class FlightIdExistente(ApiError):
    code = 412
    description = "el flightId ya existe"

class RegistroIdNoExiste(ApiError):
    code = 404
    description = "el registro por el id enviado no existe"

class CamposFaltantes(ApiError):
    code = 400
    description = "Campos faltantes en la solicitud"

class IdFormatoInvalido(ApiError):
    code = 400
    description = "El formato del id no es UUID 4"

class TrayectoNoExiste(ApiError):
    code = 404
    description = "El trayecto con ese id no existe."

class TokenInvalido(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class ErrorServicio(ApiError):
    code = 500
    description = "Error a la hora de consumir el servicio."