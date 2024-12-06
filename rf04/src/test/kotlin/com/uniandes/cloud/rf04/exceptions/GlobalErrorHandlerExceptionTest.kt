package com.uniandes.cloud.rf04.exceptions

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
    fun `test handle UnauthorizedException`() {
        val ex = UnauthorizedException()
        val expectedStatus = HttpStatus.UNAUTHORIZED.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle PostNotFoundException`() {
        val ex = PostNotFoundException()
        val expectedStatus = HttpStatus.NOT_FOUND.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle PostAlreadyExistForUser`() {
        val ex = PostAlreadyExistForUser()
        val expectedStatus = HttpStatus.PRECONDITION_FAILED.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

    @Test
    fun `test handle PostExpiredException`() {
        val ex = PostExpiredException()
        val expectedStatus = HttpStatus.PRECONDITION_FAILED.value()

        val response = globalErrorHandler.handleError(ex)

        Assertions.assertEquals(expectedStatus, response.statusCode.value())
    }

}