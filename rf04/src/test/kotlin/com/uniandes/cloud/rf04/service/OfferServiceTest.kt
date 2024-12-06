package com.uniandes.cloud.rf04.service

import com.uniandes.cloud.rf04.enums.Size
import com.uniandes.cloud.rf04.enums.UserStatus
import com.uniandes.cloud.rf04.exceptions.PostAlreadyExistForUser
import com.uniandes.cloud.rf04.exceptions.PostExpiredException
import com.uniandes.cloud.rf04.models.CurrentUser
import com.uniandes.cloud.rf04.models.Offer
import com.uniandes.cloud.rf04.models.OfferApiCallResponse
import com.uniandes.cloud.rf04.models.PostApiCallResponse
import com.uniandes.cloud.rf04.repository.OfferApiClient
import com.uniandes.cloud.rf04.repository.PostsApiClient
import com.uniandes.cloud.rf04.repository.UserApiClient
import io.mockk.Called
import io.mockk.every
import io.mockk.junit5.MockKExtension
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import java.math.BigDecimal
import java.time.LocalDateTime

@ExtendWith(MockKExtension::class)
class OfferServiceTest {


    private val userApiClient: UserApiClient = mockk()
    private val offerApiClient: OfferApiClient = mockk()
    private val postsApiClient: PostsApiClient = mockk()

    private val offerService = OfferService(userApiClient, offerApiClient, postsApiClient)

    @Test
    fun `test createPost`() {
        val postId = "postId"
        val offer = Offer(description = "description", size = Size.MEDIUM, fragile = false, offer = BigDecimal(45))
        val token = "token"
        val userId = "userId"
        val postCreatedAt = LocalDateTime.now().minusDays(1)
        val postApiCall = PostApiCallResponse(
            id = postId,
            userId = userId,
            createdAt = postCreatedAt,
            routeId = "routeId",
            expireAt = LocalDateTime.now().plusDays(10))

        val currentUser = CurrentUser(
            "id",
            "username",
            "email",
            "dni",
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )
        val offerApiCall = OfferApiCallResponse(
            createdAt = LocalDateTime.now(),
            id = "id",
            userId = "userId"
        )

        every { userApiClient.validateToken(token) } returns currentUser
        every { postsApiClient.findOfferById(postId, token) } returns postApiCall
        every { offerApiClient.createOffer(any(), token) } returns offerApiCall

        val result = offerService.createPost(postId, offer, token)

        Assertions.assertEquals("id", result.data.userId)
    }

    @Test
    fun `createPost fail - throw PostExpiredException`() {
        val postId = "postId"
        val offer = Offer(description = "description", size = Size.MEDIUM, fragile = false, offer = BigDecimal(45))
        val token = "token"
        val userId = "userId"
        val postCreatedAt = LocalDateTime.now().minusDays(1)
        val postApiCall = PostApiCallResponse(
            id = postId,
            userId = userId,
            createdAt = postCreatedAt,
            routeId = "routeId",
            expireAt = LocalDateTime.now().minusDays(10))

        val currentUser = CurrentUser(
            "id",
            "username",
            "email",
            "dni",
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )

        every { userApiClient.validateToken(token) } returns currentUser
        every { postsApiClient.findOfferById(postId, token) } returns postApiCall

        Assertions.assertThrows(PostExpiredException::class.java){
            offerService.createPost(postId, offer, token)
        }

        verify {
            offerApiClient wasNot Called
        }
    }

    @Test
    fun `createPost fail - throw PostAlreadyExistForUser`() {
        val postId = "postId"
        val offer = Offer(description = "description", size = Size.MEDIUM, fragile = false, offer = BigDecimal(45))
        val token = "token"
        val userId = "id"
        val postCreatedAt = LocalDateTime.now().minusDays(1)
        val postApiCall = PostApiCallResponse(
            id = postId,
            userId = userId,
            createdAt = postCreatedAt,
            routeId = "routeId",
            expireAt = LocalDateTime.now().minusDays(10))

        val currentUser = CurrentUser(
            "id",
            "username",
            "email",
            "dni",
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )

        every { userApiClient.validateToken(token) } returns currentUser
        every { postsApiClient.findOfferById(postId, token) } returns postApiCall

        Assertions.assertThrows(PostAlreadyExistForUser::class.java){
            offerService.createPost(postId, offer, token)
        }

        verify {
            offerApiClient wasNot Called
        }
    }
}
