package com.uniandes.cloud.rf04.models

import java.time.LocalDateTime


data class PostApiCallResponse(
    val id: String,
    val routeId: String,
    val userId: String,
    val expireAt: LocalDateTime,
    val createdAt: LocalDateTime
)