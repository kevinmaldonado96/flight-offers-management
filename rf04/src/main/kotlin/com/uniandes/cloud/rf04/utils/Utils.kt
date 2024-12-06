package com.uniandes.cloud.rf04.utils

private const val BEARER_PREFIX = "Bearer "

fun validateToken(token: String?): String? {
    if (token != null && token.startsWith(BEARER_PREFIX)) {
        return token
    }
    return null
}
