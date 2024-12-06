package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.exceptions.PostNotFoundException
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.PostApiCallResponse
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
import java.time.LocalDateTime

@ExtendWith(MockKExtension::class)
class PostApiClientTest {

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
        val postId = "postId"
        val restTemplate = mockk<RestTemplate>()
        val postsApiClient = PostsApiClient(restTemplate, apiPropertiesConfig)
        val token = "validToken"
        val postApiCallResponse = PostApiCallResponse(
            createdAt = LocalDateTime.now(),
            id = "id",
            expireAt = LocalDateTime.now(),
            routeId = "routeId",
            userId = "userId"
        )
        every {
            restTemplate.exchange(any<RequestEntity<*>>(), PostApiCallResponse::class.java)
        } returns ResponseEntity.ok(postApiCallResponse)
        val result = postsApiClient.findOfferById(postId, token)

        Assertions.assertNotNull(result)
    }

    @Test
    fun `create offer throw UnauthorizedException when token is invalid`() {
        val postId = "postId"
        val restTemplate = mockk<RestTemplate>()
        val postsApiClient = PostsApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), PostApiCallResponse::class.java)
        } throws HttpClientErrorException(HttpStatus.UNAUTHORIZED)

        Assertions.assertThrows(UnauthorizedException::class.java) {
            postsApiClient.findOfferById(postId, token)
        }
    }

    @Test
    fun `create offer throw Exception when token is invalid`() {
        val postId = "postId"
        val restTemplate = mockk<RestTemplate>()
        val postsApiClient = PostsApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), PostApiCallResponse::class.java)
        } throws HttpClientErrorException(HttpStatus.INTERNAL_SERVER_ERROR)

        Assertions.assertThrows(Exception::class.java) {
            postsApiClient.findOfferById(postId, token)
        }
    }

    @Test
    fun `create offer throw NotFoundException when post does not exist`() {
        val postId = "postId"
        val restTemplate = mockk<RestTemplate>()
        val postsApiClient = PostsApiClient(restTemplate, apiPropertiesConfig)
        val token = "invalidToken"

        every {
            restTemplate.exchange(any<RequestEntity<*>>(), PostApiCallResponse::class.java)
        } throws HttpClientErrorException(HttpStatus.NOT_FOUND)

        Assertions.assertThrows(PostNotFoundException::class.java) {
            postsApiClient.findOfferById(postId, token)
        }
    }
    
}