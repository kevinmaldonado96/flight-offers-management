package com.uniandes.cloud.rf04.controller

import com.ninjasquad.springmockk.MockkBean
import com.uniandes.cloud.rf04.models.OfferApiResponse
import com.uniandes.cloud.rf04.service.OfferService
import io.mockk.clearAllMocks
import io.mockk.every
import io.mockk.junit5.MockKExtension
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders
import org.springframework.test.web.servlet.result.MockMvcResultHandlers
import org.springframework.test.web.servlet.result.MockMvcResultMatchers
import java.time.LocalDateTime

@ExtendWith(MockKExtension::class)
@WebMvcTest(OfferController::class)
class OfferControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockkBean
    private lateinit var offerService: OfferService



    @BeforeEach
    fun beforeEach() {
        clearAllMocks()
    }

    @Test
    fun `create user success`() {
        val token = "Bearer 1234567890"
        val response = OfferApiResponse(
            data = OfferApiResponse.Data(
                id = "id",
                userId = "userId",
                createdAt = LocalDateTime.now(),
                postId = "postId"
            ),
            msg = "message"
        )
        every { offerService.createPost(any(), any(), any()) } returns response

        mockMvc.perform(
            MockMvcRequestBuilders.post("/rf004/posts/123/offers")
                .header("Authorization", token)
                .content(
                    """
                        {
                          "description": "description",
                          "size": "LARGE",
                          "fragile": false,
                          "offer": 700
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isCreated)
    }

    @Test
    fun `create user fail - token was not sent`() {
        mockMvc.perform(
            MockMvcRequestBuilders.post("/rf004/posts/123/offers")
                .content(
                    """
                        {
                          "description": "description",
                          "size": "LARGE",
                          "fragile": false,
                          "offer": 700
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isForbidden)
    }

    @Test
    fun `create user fail - wrong token`() {
        mockMvc.perform(
            MockMvcRequestBuilders.post("/rf004/posts/123/offers")
                .header("Authorization", "123456")
                .content(
                    """
                        {
                          "description": "description",
                          "size": "LARGE",
                          "fragile": false,
                          "offer": 700
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isUnauthorized)
    }

    @Test
    fun `create user fail - empty token`() {
        mockMvc.perform(
            MockMvcRequestBuilders.post("/rf004/posts/123/offers")
                .header("Authorization", "")
                .content(
                    """
                        {
                          "description": "description",
                          "size": "LARGE",
                          "fragile": false,
                          "offer": 700
                        }
                    """.trimIndent()
                )
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isForbidden)
    }

    @Test
    fun `ping`() {
        mockMvc.perform(
            MockMvcRequestBuilders.post("/rf004/posts/ping")
                .contentType(MediaType.APPLICATION_JSON))
            .andDo(MockMvcResultHandlers.print())
            .andExpect(MockMvcResultMatchers.status().isOk)
    }

}