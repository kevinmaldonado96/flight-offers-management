package com.uniandes.cloud.native_.utils

import java.security.MessageDigest
import java.security.SecureRandom
import java.util.*

fun generatePasswordHash(password: String, salt: ByteArray): String {
    val md = MessageDigest.getInstance("SHA-256")
    md.update(salt)
    val hashedPassword = md.digest(password.toByteArray())
    return Base64.getEncoder().encodeToString(hashedPassword)
}

fun validatePassword(password: String, salt: ByteArray, storedHash: String): Boolean {
    val hashToValidate = generatePasswordHash(password, salt)
    return hashToValidate == storedHash
}

fun generateSalt(): ByteArray {
    val random = SecureRandom()
    val salt = ByteArray(16)
    random.nextBytes(salt)
    return salt
}

fun validateEmailFormat(email: String): Boolean {
    val regex = Regex("^\\S+@\\S+\\.\\S+$")
    return regex.matches(email)
}

private const val BEARER_PREFIX = "Bearer "

fun validateToken(token: String?): String? {
    if (token != null && token.startsWith(BEARER_PREFIX)) {
        return token.substring(BEARER_PREFIX.length)
    }
    return null
}