package com.uniandes.cloud.native_.models

import com.uniandes.cloud.native_.enums.UserStatus
import java.time.LocalDateTime

data class User(
        val id: String,
        val username: String,
        val password: String,
        val email: String,
        val dni: String?,
        val salt: ByteArray,
        val fullName: String?,
        val phoneNumber: String?,
        val status: UserStatus?,
        val token: String?,
        val expireAt: LocalDateTime?,
        val createAt: LocalDateTime
) {
        override fun equals(other: Any?): Boolean {
                if (this === other) return true
                if (javaClass != other?.javaClass) return false

                other as User

                if (id != other.id) return false
                if (username != other.username) return false
                if (password != other.password) return false
                if (email != other.email) return false
                if (dni != other.dni) return false
                if (!salt.contentEquals(other.salt)) return false
                if (fullName != other.fullName) return false
                if (phoneNumber != other.phoneNumber) return false
                if (createAt != other.createAt) return false

                return true
        }

        override fun hashCode(): Int {
                var result = id.hashCode()
                result = 31 * result + username.hashCode()
                result = 31 * result + password.hashCode()
                result = 31 * result + email.hashCode()
                result = 31 * result + (dni?.hashCode() ?: 0)
                result = 31 * result + (salt.contentHashCode())
                result = 31 * result + (fullName?.hashCode() ?: 0)
                result = 31 * result + phoneNumber.hashCode()
                result = 31 * result + createAt.hashCode()
                return result
        }
}

data class UserCreateRequestBody(
        val username: String,
        val password: String,
        val email: String,
        val dni: String?,
        val fullName: String?,
        val phoneNumber: String?
)

data class UserUpdateRequestBody(
        val status: UserStatus?,
        val dni: String?,
        val fullName: String?,
        val phoneNumber: String?
)

data class UserAfterCreate(
        val id: String,
        val createdAt: LocalDateTime
)

data class CurrentUser(
        val id: String,
        val username: String,
        val email: String,
        val dni: String?,
        val fullName: String?,
        val phoneNumber: String?,
        val status: UserStatus?
)

fun User.toResponseAfterCreate(): UserAfterCreate =
        UserAfterCreate(
                id = this.id.toString(),
                createdAt = this.createAt
        )


fun UserUpdateRequestBody.hasAttributesNotNull(): Boolean {
        return this.status != null ||
                this.fullName != null ||
                this.dni != null ||
                this.phoneNumber != null
}

fun User.toCurrentUser() = CurrentUser(
        id = this.id,
        username = this.username,
        email = this.email,
        fullName = this.fullName,
        dni = this.dni,
        phoneNumber = this.phoneNumber,
        status = this.status
)