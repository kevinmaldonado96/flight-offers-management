class ApiError(Exception):
    code = 422
    description = "Default message"

class TokenError(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class NotFoundError(ApiError):
    code = 404
    description = "La publicación con ese id no existe."

class UnauthorizedError(ApiError):
    code = 401
    description = "El token no es válido o está vencido."


class BadRequestError(ApiError):
    code = 400
    description = "En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado."


class DateTypeError(ApiError):
    code = 412
    description = "La fecha expiración no es válida"

class ServiceError(ApiError):
    code = 500
    description = "Error a la hora de consumir el servicio."
