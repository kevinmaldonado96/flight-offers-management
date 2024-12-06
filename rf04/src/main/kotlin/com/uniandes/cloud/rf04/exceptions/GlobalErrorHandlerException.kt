package com.uniandes.cloud.rf04.exceptions

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

    @ExceptionHandler(UnauthorizedException::class)
    fun handleError(ex: UnauthorizedException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.UNAUTHORIZED)
    }

    @ExceptionHandler(PostNotFoundException::class)
    fun handleError(ex: PostNotFoundException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(PostAlreadyExistForUser::class)
    fun handleError(ex: PostAlreadyExistForUser): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
    }

    @ExceptionHandler(PostExpiredException::class)
    fun handleError(ex: PostExpiredException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
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