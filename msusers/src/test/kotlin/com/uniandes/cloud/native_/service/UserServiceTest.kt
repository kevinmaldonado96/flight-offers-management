package com.uniandes.cloud.native_.service

import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.exceptions.*
import com.uniandes.cloud.native_.models.DefaultResponse
import com.uniandes.cloud.native_.models.User
import com.uniandes.cloud.native_.models.UserAfterCreate
import com.uniandes.cloud.native_.models.toCurrentUser
import com.uniandes.cloud.native_.repository.UserRepository
import com.uniandes.cloud.native_.utils.generatePasswordHash
import io.mockk.*
import io.mockk.impl.annotations.InjectMockKs
import io.mockk.impl.annotations.MockK
import io.mockk.junit5.MockKExtension
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import java.time.LocalDateTime
import java.util.*

@ExtendWith(MockKExtension::class)
class UserServiceTest {

    @InjectMockKs
    private lateinit var userService: UserService

    @MockK
    private lateinit var userRepository: UserRepository

    @BeforeEach
    fun setup(){
        clearAllMocks()
    }

    @Test
    fun `save should throw RecordAlreadyExistException when username already exists`() {

        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )

        every {  userRepository.findByUsername(any()) } returns Optional.of(user)

        Assertions.assertThrows(RecordAlreadyExistException::class.java) {
            userService.save("username", "password", "email@example.com", null, null, null)
        }
    }

    @Test
    fun `save should throw RecordAlreadyExistException when email already exists`() {
        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )

        every {  userRepository.findByUsername(any()) } returns Optional.empty()
        every {  userRepository.findByEmail(any()) } returns Optional.of(user)

        Assertions.assertThrows(RecordAlreadyExistException::class.java) {
            userService.save("username", "password", "email", null, null, null)
        }
    }

    @Test
    fun `save should throw UsernameWithWhiteSpacesCharactersException when username contains spaces`() {
        every {  userRepository.findByUsername(any()) } returns Optional.empty()
        every {  userRepository.findByEmail(any()) } returns Optional.empty()
        Assertions.assertThrows(UsernameWithWhiteSpacesCharactersException::class.java) {
            userService.save("user name", "password", "email@example.com", null, null, null)
        }
    }

    @Test
    fun `save should throw InvalidEmailFormatException when email format is invalid`() {
        every {  userRepository.findByUsername(any()) } returns Optional.empty()
        every {  userRepository.findByEmail(any()) } returns Optional.empty()
        Assertions.assertThrows(InvalidEmailFormatException::class.java) {
            userService.save("username", "password", "invalid_email", null, null, null)
        }
    }

    @Test
    fun `save successful`() {
        val response = UserAfterCreate("id", LocalDateTime.now().withNano(0))
        every { userRepository.save(any(), any(), any(), any(), any(), any()) } returns response
        every {  userRepository.findByUsername(any()) } returns Optional.empty()
        every {  userRepository.findByEmail(any()) } returns Optional.empty()

        userService.save("username", "password", "email@gmail.com", "dni", "fullName", "phoneNumber")

        verify (exactly = 1){
            userRepository.save(
                match { "username" == it },
                match { "password" == it },
                match { "email@gmail.com" == it },
                match { "dni" == it },
                match { "fullName" == it },
                match { "phoneNumber" == it },
            )
        }
    }

    @Test
    fun `test update method should throw UserDoesNotExistException when user is not found`() {

        val id = "123"
        every { userRepository.findById(id) } returns Optional.empty()


        Assertions.assertThrows(UserDoesNotExistException::class.java) {
            userService.update(id, UserStatus.NO_VERIFICADO, "123456789", "John Doe", "1234567890")
        }
    }

    @Test
    fun `test update method should call userRepository update`() {
        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )

        val id = "123"
        val status = UserStatus.NO_VERIFICADO
        val dni = "123456789"
        val fullName = "John Doe"
        val phoneNumber = "1234567890"
        every { userRepository.findById(id) } returns Optional.of(user)
        every { userRepository.update(id, status, dni, fullName, phoneNumber) } returns DefaultResponse("Success")

        val result = userService.update(id, status, dni, fullName, phoneNumber)

        Assertions.assertEquals("Success", result.msg)
        verify(exactly = 1) {
            userRepository.findById(id)
            userRepository.update(id, status, dni, fullName, phoneNumber)
        }
    }

    @Test
    fun `test currentUser method should throw UnauthorizedException when user is not found`() {

        val token = ""
        every { userRepository.findByToken(token) } returns Optional.empty()


        Assertions.assertThrows(UnauthorizedException::class.java) {
            userService.currentUser(token)
        }
    }

    @Test
    fun `test currentUser method should return CurrentUser when user is found`() {
        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )


        val token = "validToken"

        every { userRepository.findByToken(token) } returns Optional.of(user)

        val result = userService.currentUser(token)

        Assertions.assertEquals(user.toCurrentUser(), result)
    }

    @Test
    fun `test resetData method should call resetTable`() {

        every { userRepository.resetTable() } just runs
        userService.resetData()

        verify(exactly = 1) { userRepository.resetTable() }
    }

    @Test
    fun `test login method should throw InvalidUsernameOrPasswordException when user is not found`() {

        val username = "invalidUsername"
        every { userRepository.findByUsername(username) } returns Optional.empty()

        Assertions.assertThrows(InvalidUsernameOrPasswordException::class.java) {
            userService.login(username, "password")
        }
    }

    @Test
    fun `test login method should throw InvalidUsernameOrPasswordException when password is invalid`() {
        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )

        val username = "validUsername"

        every { userRepository.findByUsername(username) } returns Optional.of(user)

        Assertions.assertThrows(InvalidUsernameOrPasswordException::class.java) {
            userService.login(username, "invalidPassword")
        }
    }

    @Test
    fun `test login method should return Session when login is successful`() {
        val user = User(
            "id",
            "username",
            generatePasswordHash("password", "salt".toByteArray()),
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )
        val username = "validUsername"
        val password = "password"

        every { userRepository.findByUsername(username) } returns Optional.of(user)
        every { userRepository.updateAuth(username, any(), any()) } returns true

        val result = userService.login(username, password)

        Assertions.assertEquals(user.id, result.id)
    }

    @Test
    fun `test login method should throw InvalidUsernameOrPasswordException when updateAuth fails`() {
        val user = User(
            "id",
            "username",
            "password",
            "email",
            "dni",
            "salt".toByteArray(),
            "fullName",
            "phoneNumber",
            UserStatus.NO_VERIFICADO,
            "token",
            LocalDateTime.now().withNano(0),
            LocalDateTime.now().withNano(0)
        )
        val username = "validUsername"
        val password = "validPassword"

        every { userRepository.findByUsername(username) } returns Optional.of(user)
        every { userRepository.updateAuth(username, any(), any()) } returns false

        Assertions.assertThrows(InvalidUsernameOrPasswordException::class.java) {
            userService.login(username, password)
        }
    }

}