package com.uniandes.cloud.rf04.models

import com.uniandes.cloud.rf04.enums.Size
import java.math.BigDecimal
import java.time.LocalDateTime

data class OfferRequestBody (
    val description: String,
    val size: Size,
    val fragile: Boolean,
    val offer: BigDecimal
)

data class Offer(
    val description: String,
    val size: Size,
    val fragile: Boolean,
    val offer: BigDecimal
)

data class OfferApiCallResponse(
    val createdAt: LocalDateTime,
    val id: String,
    val userId: String
)

data class OfferApiClientRequestBody(
    val postId: String,
    val description: String,
    val size: Size,
    val fragile: Boolean,
    val offer: BigDecimal
)

data class OfferApiResponse(
    val data: Data,
    val msg: String
) {
    data class Data(
        val id: String,
        val userId: String,
        val createdAt: LocalDateTime,
        val postId: String
    )
}

fun OfferRequestBody.toOffer() = Offer(
    description = this.description,
    size = this.size,
    fragile = this.fragile,
    offer = this.offer
)
