package com.uniandes.cloud.native_.service

import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.exceptions.*
import com.uniandes.cloud.native_.models.*
import com.uniandes.cloud.native_.repository.IUserRepository
import com.uniandes.cloud.native_.utils.validateEmailFormat
import com.uniandes.cloud.native_.utils.validatePassword
import org.springframework.stereotype.Service
import java.time.LocalDateTime
import java.util.*

@Service
class UserService(
        private val userRepository: IUserRepository
) {

     fun save(username: String,
             password: String,
             email: String,
             dni: String?,
             fullName: String?,
             phoneNumber: String?): UserAfterCreate {

         userRepository.findByUsername(username).ifPresent {
             throw RecordAlreadyExistException()
         }

         userRepository.findByEmail(email).ifPresent {
             throw RecordAlreadyExistException()
         }

         if (username.contains(" "))
             throw UsernameWithWhiteSpacesCharactersException()

         if (!validateEmailFormat(email))
             throw InvalidEmailFormatException()

        return userRepository.save(username, password, email, dni, fullName, phoneNumber)
    }

    fun update(id: String,
               status: UserStatus?,
               dni: String?,
               fullName: String?,
               phoneNumber: String?): DefaultResponse {

        userRepository.findById(id).orElseThrow{
            UserDoesNotExistException()
        }

        return userRepository.update(id, status, dni, fullName, phoneNumber)
    }

    fun currentUser(token: String): CurrentUser {
        val user = userRepository.findByToken(token).orElseThrow {
            UnauthorizedException()
        }
        return user.toCurrentUser()
    }

    fun resetData() {
        userRepository.resetTable()
    }

    fun login(username: String, password: String): Session {

        val user = userRepository.findByUsername(username).orElseThrow {
            InvalidUsernameOrPasswordException()
        }

        if (!validatePassword(password, user.salt, user.password))
            throw InvalidUsernameOrPasswordException()

        val tokenExpiredAt = LocalDateTime.now().plusDays(1)
        val token = UUID.randomUUID().toString()

        userRepository.updateAuth(username, token, tokenExpiredAt)
        return Session(
            user.id,
            token,
            tokenExpiredAt.toString()
        )
    }

}

