package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.exceptions.PostNotFoundException
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.PostApiCallResponse
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.RequestEntity
import org.springframework.stereotype.Component
import org.springframework.web.client.HttpClientErrorException
import org.springframework.web.client.RestTemplate

@Component
class PostsApiClient(
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun findOfferById(postId: String, token: String): PostApiCallResponse {

        val url = "${apiPropertiesConfig.post.baseUrl}/${apiPropertiesConfig.post.paths.findById.replace("#{post_id}", postId)}"

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .get(url)
            .headers(headers)
            .build()

        try {
            val response = restTemplate.exchange(request, PostApiCallResponse::class.java).body!!
            return response
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                HttpStatus.NOT_FOUND -> throw PostNotFoundException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}