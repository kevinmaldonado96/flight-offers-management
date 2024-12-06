package com.uniandes.cloud.native_.repository

import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.models.DefaultResponse
import com.uniandes.cloud.native_.models.User
import com.uniandes.cloud.native_.models.UserAfterCreate
import java.time.LocalDateTime
import java.util.*

interface IUserRepository {

    fun save(username: String,
                     password: String,
                     email: String,
                     dni: String?,
                     fullName: String?,
                     phoneNumber: String?): UserAfterCreate

    fun findByUsername(username: String): Optional<User>
    fun findByEmail(email: String): Optional<User>

    fun findById(id: String): Optional<User>

    fun update(id: String,
               status: UserStatus?,
               dni: String?,
               fullName: String?,
               phoneNumber: String?): DefaultResponse

    fun findByToken(token: String): Optional<User>

    fun resetTable()

    fun updateAuth(username: String, token: String, expireAt: LocalDateTime): Boolean

}