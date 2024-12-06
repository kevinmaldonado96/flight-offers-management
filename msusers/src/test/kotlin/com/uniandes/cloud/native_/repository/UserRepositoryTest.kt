package com.uniandes.cloud.native_.repository

import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.models.UserAfterCreate
import com.uniandes.cloud.native_.test_database.deleteAllTestData
import io.mockk.clearAllMocks
import io.mockk.impl.annotations.InjectMockKs
import io.mockk.junit5.MockKExtension
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import java.time.LocalDateTime
import java.util.*

@ExtendWith(MockKExtension::class)
class UserRepositoryTest{

    @InjectMockKs
    private lateinit var userRepository: UserRepository

    @BeforeEach
    fun setUp() {
        clearAllMocks()
        deleteAllTestData()
    }

    @Test
    fun `save method should insert user entity`() {
        val username = "username"
        val password = "password"
        val email = "email"
        val dni = "dni"
        val fullName = "fullName"
        val phoneNumber = "phoneNumber"

        val userNew = createUser(username, password, email, dni, fullName, phoneNumber)

        val userStored = userRepository.findById(userNew.id)

        Assertions.assertEquals("username", userStored.get().username)
        Assertions.assertNotNull(userStored.get().password)
        Assertions.assertNotNull(userStored.get().salt)
        Assertions.assertEquals("email", userStored.get().email)
        Assertions.assertEquals("dni", userStored.get().dni)
        Assertions.assertEquals("fullName", userStored.get().fullName)
        Assertions.assertEquals("phoneNumber", userStored.get().phoneNumber)
    }

    @Test
    fun `update method should modify user`() {
        val username = "username"
        val password = "password"
        val email = "email"
        var dni = "dni"
        var fullName = "fullName"
        var phoneNumber = "phoneNumber"

        val userNew = createUser(username, password, email, dni, fullName, phoneNumber)
        val storedUser = userRepository.findByUsername(username).get()
        dni = "123"
        fullName = "nombre completo"
        phoneNumber = "1234567890"
        userRepository.update(userNew.id, UserStatus.NO_VERIFICADO, dni, fullName, phoneNumber)

        val userModified = userRepository.findByEmail(email).get()

        Assertions.assertEquals(userModified.id, storedUser.id)
        Assertions.assertNotEquals(userModified.dni, storedUser.dni)
        Assertions.assertNotEquals(userModified.fullName, storedUser.fullName)
        Assertions.assertNotEquals(userModified.phoneNumber, storedUser.phoneNumber)
    }

    @Test
    fun `updateAuth method should modify user`() {
        val username = "username"
        val password = "password"
        val email = "email"
        var dni = "dni"
        var fullName = "fullName"
        var phoneNumber = "phoneNumber"

        createUser(username, password, email, dni, fullName, phoneNumber)
        val storedUser = userRepository.findByUsername(username).get()

        val token = UUID.randomUUID().toString()
        val expireAt = LocalDateTime.now().withNano(0)
        val isSuccess = userRepository.updateAuth(storedUser.username, token, expireAt)

        val userModified = userRepository.findByToken(token).get()

        Assertions.assertTrue(isSuccess)
        Assertions.assertEquals(expireAt, userModified.expireAt)
        Assertions.assertEquals(token, userModified.token)

    }

    @Test
    fun `updateAuth user does not exist then method should not modify`() {
        val username = "username"
        val password = "password"
        val email = "email"
        var dni = "dni"
        var fullName = "fullName"
        var phoneNumber = "phoneNumber"

        createUser(username, password, email, dni, fullName, phoneNumber)

        val token = UUID.randomUUID().toString()
        val expireAt = LocalDateTime.now().withNano(0)
        val isSuccess = userRepository.updateAuth("random", token, expireAt)

        Assertions.assertFalse(isSuccess)
    }

    @Test
    fun `reset table`() {
        val username = "username"
        val password = "password"
        val email = "email"
        var dni = "dni"
        var fullName = "fullName"
        var phoneNumber = "phoneNumber"

        createUser(username, password, email, dni, fullName, phoneNumber)
        val userBeforeDelete = userRepository.findByUsername(username)

        userRepository.resetTable()

        val userAfterDelete = userRepository.findByUsername(username)

        Assertions.assertFalse(userBeforeDelete.isEmpty)
        Assertions.assertTrue(userAfterDelete.isEmpty)

    }

    private fun createUser(username: String,
                           password: String,
                           email: String,
                           dni: String,
                           fullName: String,
                           phoneNumber: String): UserAfterCreate {
        return userRepository.save(username, password, email, dni, fullName, phoneNumber)
    }
}