package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.enums.Size
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.OfferApiCallResponse
import com.uniandes.cloud.rf04.models.OfferApiClientRequestBody
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
import java.math.BigDecimal
import java.time.LocalDateTime

@ExtendWith(MockKExtension::class)
class OfferApiClientTest {

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
    fun `create offer successful`() {

        val restTemplate = mockk<RestTemplate>()
        val offerApiClient = OfferApiClient(restTemplate, apiPropertiesConfig)
        val token = "validToken"
        val offerApiCallResponse = OfferApiCallResponse(
            createdAt = LocalDateTime.now(),
            id = "id",
            userId = "userId"
        )
        val offerApiClientRequestBody = OfferApiClientRequestBody(
            description = "description",
            postId= "postId",
            size = Size.LARGE,
            fragile = true,
            offer = BigDecimal(550)
        )

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), OfferApiCallResponse::class.java)
        } returns ResponseEntity.ok(offerApiCallResponse)
        val result = offerApiClient.createOffer(offerApiClientRequestBody, token)

        Assertions.assertNotNull(result)
    }

    @Test
    fun `validateToken should throw UnauthorizedException when token is invalid`() {
        val restTemplate = mockk<RestTemplate>()
        val offerApiClient = OfferApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"
        val offerApiClientRequestBody = OfferApiClientRequestBody(
            description = "description",
            postId= "postId",
            size = Size.LARGE,
            fragile = true,
            offer = BigDecimal(550)
        )

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), OfferApiCallResponse::class.java)
        } throws HttpClientErrorException(HttpStatus.UNAUTHORIZED)

        Assertions.assertThrows(UnauthorizedException::class.java) {
            offerApiClient.createOffer(offerApiClientRequestBody, token)
        }
    }

    @Test
    fun `validateToken should throw Exception when token is invalid`() {
        val restTemplate = mockk<RestTemplate>()
        val offerApiClient = OfferApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"
        val offerApiClientRequestBody = OfferApiClientRequestBody(
            description = "description",
            postId= "postId",
            size = Size.LARGE,
            fragile = true,
            offer = BigDecimal(550)
        )

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), OfferApiCallResponse::class.java)
        } throws HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR)

        Assertions.assertThrows(Exception::class.java) {
            offerApiClient.createOffer(offerApiClientRequestBody, token)
        }
    }
}