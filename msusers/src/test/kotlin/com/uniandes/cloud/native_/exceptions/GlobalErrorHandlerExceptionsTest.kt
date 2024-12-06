package com.uniandes.cloud.native_.exceptions

import io.mockk.impl.annotations.InjectMockKs
import io.mockk.junit5.MockKExtension
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.springframework.http.HttpStatus

@ExtendWith(MockKExtension::class)
class GlobalErrorHandlerExceptionsTest {

    @InjectMockKs
    private lateinit var globalErrorHandler: GlobalErrorHandlerException

    @Test
    fun `test handle HeaderNotFoundException`() {
        val ex = HeaderNotFoundException()
        val expectedStatus = HttpStatus.FORBIDDEN.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle UsernameWithWhiteSpacesCharactersException`() {
        val ex = UsernameWithWhiteSpacesCharactersException()
        val expectedStatus = HttpStatus.BAD_REQUEST.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle InvalidEmailFormatException`() {
        val ex = InvalidEmailFormatException()
        val expectedStatus = HttpStatus.BAD_REQUEST.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle RecordAlreadyExistException`() {
        val ex = RecordAlreadyExistException()
        val expectedStatus = HttpStatus.PRECONDITION_FAILED.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle UserDoesNotExistException`() {
        val ex = UserDoesNotExistException()
        val expectedStatus = HttpStatus.NOT_FOUND.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle InvalidUsernameOrPasswordException`() {
        val ex = InvalidUsernameOrPasswordException()
        val expectedStatus = HttpStatus.NOT_FOUND.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle UnauthorizedException`() {
        val ex = UnauthorizedException()
        val expectedStatus = HttpStatus.UNAUTHORIZED.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

}