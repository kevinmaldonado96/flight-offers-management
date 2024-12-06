package com.uniandes.cloud.native_.exceptions

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler

@ControllerAdvice
class GlobalErrorHandlerException {

    @ExceptionHandler(HeaderNotFoundException::class)
    fun handleError(ex: HeaderNotFoundException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.FORBIDDEN)
    }

    @ExceptionHandler(UsernameWithWhiteSpacesCharactersException::class)
    fun handleError(ex: UsernameWithWhiteSpacesCharactersException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(InvalidEmailFormatException::class)
    fun handleError(ex: InvalidEmailFormatException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(RecordAlreadyExistException::class)
    fun handleError(ex: RecordAlreadyExistException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
    }

    @ExceptionHandler(UserDoesNotExistException::class)
    fun handleError(ex: UserDoesNotExistException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(InvalidUsernameOrPasswordException::class)
    fun handleError(ex: InvalidUsernameOrPasswordException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(UnauthorizedException::class)
    fun handleError(ex: UnauthorizedException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.UNAUTHORIZED)
    }

    fun handleError(
        responseStatus: HttpStatus,
    ): ResponseEntity<RequestFailure> {
        return ResponseEntity(
            RequestFailure(responseStatus.value()),
            responseStatus
        )
    }
}
data class RequestFailure(val status: Int)