package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.enums.UserStatus
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.CurrentUser
import io.mockk.clearAllMocks
import io.mockk.every
import io.mockk.junit5.MockKExtension
import io.mockk.mockk
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.springframework.http.HttpStatus
import org.springframework.http.RequestEntity
import org.springframework.http.ResponseEntity
import org.springframework.web.client.HttpClientErrorException
import org.springframework.web.client.RestTemplate

@ExtendWith(MockKExtension::class)
class UserApiClientTest {

    @BeforeEach
    fun beforeEach(){
        clearAllMocks()
    }



    private  val apiPropertiesConfig = ApiPropertiesConfig(
        offer = ApiPropertiesConfig.Offer(
            baseUrl = "base-url"
        ),
        user = ApiPropertiesConfig.User(
            baseUrl = "base-url",
            paths = ApiPropertiesConfig.UserPath(
                validateToken = "validate-token"
            )
        ),
        post = ApiPropertiesConfig.Post(
            baseUrl = "base-url",
            paths = ApiPropertiesConfig.PostPaths(
                findById = "find-by-id"
            )
        )
    )

    @Test
    fun `validateToken should return CurrentUser when token is valid`() {

        val restTemplate = mockk<RestTemplate>()
        val userApiClient = UserApiClient(restTemplate, apiPropertiesConfig)
        val token = "validToken"
        val currentUser = CurrentUser(
            "id",
            "username",
            "email",
            "dni",
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), CurrentUser::class.java)
        } returns ResponseEntity.ok(currentUser)
        val result = userApiClient.validateToken(token)

        Assertions.assertNotNull(result)
    }

    @Test
    fun `validateToken should throw UnauthorizedException when token is invalid`() {
        val restTemplate = mockk<RestTemplate>()
        val userApiClient = UserApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), CurrentUser::class.java)
        } throws HttpClientErrorException(HttpStatus.UNAUTHORIZED)

        Assertions.assertThrows(UnauthorizedException::class.java) {
            userApiClient.validateToken(token)
        }
    }

    @Test
    fun `validateToken should throw Exception when token is invalid`() {
        val restTemplate = mockk<RestTemplate>()
        val userApiClient = UserApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), CurrentUser::class.java)
        } throws HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR)

        Assertions.assertThrows(Exception::class.java) {
            userApiClient.validateToken(token)
        }
    }
}
