package com.uniandes.cloud.native_.models

data class Credentials(
        val username: String,
        val password: String
)

data class Session(
        val id: String,
        val token: String,
        val expireAt: String
)