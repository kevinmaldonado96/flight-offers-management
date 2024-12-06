package com.uniandes.cloud.rf04.service

import com.uniandes.cloud.rf04.exceptions.PostAlreadyExistForUser
import com.uniandes.cloud.rf04.exceptions.PostExpiredException
import com.uniandes.cloud.rf04.models.Offer
import com.uniandes.cloud.rf04.models.OfferApiClientRequestBody
import com.uniandes.cloud.rf04.models.OfferApiResponse
import com.uniandes.cloud.rf04.repository.OfferApiClient
import com.uniandes.cloud.rf04.repository.PostsApiClient
import com.uniandes.cloud.rf04.repository.UserApiClient
import org.springframework.stereotype.Service
import java.time.LocalDateTime

@Service
class OfferService (
    private val userApiClient: UserApiClient,
    private val offerApiClient: OfferApiClient,
    private val postsApiClient: PostsApiClient,
){

    fun createPost(postId: String, offer: Offer, token: String): OfferApiResponse {
        val currentUser = userApiClient.validateToken(token)
        val postApiCall = postsApiClient.findOfferById(postId, token)

        if (currentUser.id == postApiCall.userId)
            throw PostAlreadyExistForUser()

        if (postApiCall.expireAt.isBefore(LocalDateTime.now()))
            throw PostExpiredException()

        val offerApiCall = offerApiClient.createOffer(
            OfferApiClientRequestBody(
                postId = postApiCall.id,
                description = offer.description,
                size = offer.size,
                fragile = offer.fragile,
                offer = offer.offer
            ),
            token
        )
        return OfferApiResponse(
            data = OfferApiResponse.Data(
                offerApiCall.id,
                currentUser.id,
                postApiCall.createdAt,
                postApiCall.id
            ),
            msg = "message"
        )
    }
}