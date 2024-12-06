package com.uniandes.cloud.native_.controller

import com.ninjasquad.springmockk.MockkBean
import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.models.CurrentUser
import com.uniandes.cloud.native_.models.DefaultResponse
import com.uniandes.cloud.native_.models.Session
import com.uniandes.cloud.native_.models.UserAfterCreate
import com.uniandes.cloud.native_.service.UserService
import io.mockk.every
import io.mockk.junit5.MockKExtension
import io.mockk.just
import io.mockk.runs
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.mock.mockito.MockBean
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.ResultHandler
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders
import org.springframework.test.web.servlet.result.MockMvcResultHandlers
import org.springframework.test.web.servlet.result.MockMvcResultMatchers
import java.time.LocalDateTime

@ExtendWith(MockKExtension::class)
@WebMvcTest(UserController::class)
class UserControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockkBean
    private lateinit var userService: UserService

    @Test
    fun `create user success`() {
        val response = UserAfterCreate(
            "id",
            LocalDateTime.now().withNano(0)
        )
        every { userService.save(any(), any(), any(), any(), any(), any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.post("/users")
                .content(
                    """
                        {
                          "username": "nombredeusuario",
                          "password": "password",
                          "email": "email@uniandes.edu.co",
                          "dni": "identificación",
                          "fullName": "nombre completo del usuario",
                          "phoneNumber": "número de teléfono"
                        }
                    """.trimIndent()
                )
            .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isCreated)
    }

    @Test
    fun `update user success`() {
        val response = DefaultResponse(
            "Usuario actualizado exitosamente"
        )
        every { userService.update(any(), any(), any(), any(), any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.patch("/users/1")
                .content(
                    """
                        {
                          "status": "NO_VERIFICADO",
                          "dni": "identificación",
                          "fullName": "nombre completo del usuario",
                          "phoneNumber": "número de teléfono"
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }

    @Test
    fun `update user fail - all attributes are null`() {
        val response = DefaultResponse(
            "Usuario actualizado exitosamente"
        )
        every { userService.update(any(), any(), any(), any(), any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.patch("/users/1")
                .content(
                    """
                        {
                          "status": null,
                          "dni": null,
                          "fullName": null,
                          "phoneNumber": null
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isBadRequest)
    }

    @Test
    fun `Auth successful`() {
        val response = Session(
            "id",
            "token",
            LocalDateTime.now().withNano(0).plusDays(1).toString()
        )
        every { userService.login(any(), any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.post("/users/auth")
                .content(
                    """
                        {
                          "username": "nombredeusuario",
                          "password": "password"
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }

    @Test
    fun `current user successful`() {
        val token = "Bearer 1234567890"
        val response = CurrentUser(
            "id",
            "token",
            "email",
            "dni",
            "fullname",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )
        every { userService.currentUser(any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.get("/users/me")
                .header("Authorization", token)
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }

    @Test
    fun `current user fail - token was not sent`() {
        val response = CurrentUser(
            "id",
            "token",
            "email",
            "dni",
            "fullname",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )
        every { userService.currentUser(any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.get("/users/me")
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isForbidden)
    }

    @Test
    fun `current user fail - token is empty`() {
        val response = CurrentUser(
            "id",
            "token",
            "email",
            "dni",
            "fullname",
            "phoneNumber",
            UserStatus.NO_VERIFICADO
        )
        every { userService.currentUser(any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.get("/users/me")
                .header("Authorization", "")
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isForbidden)
    }

    @Test
    fun `ping successful`() {
        mockMvc.perform(
            MockMvcRequestBuilders.get("/users/ping")
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }

    @Test
    fun `reset table successful`() {

        every { userService.resetData() } just runs

        mockMvc.perform(
            MockMvcRequestBuilders.post("/users/reset")
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }
}