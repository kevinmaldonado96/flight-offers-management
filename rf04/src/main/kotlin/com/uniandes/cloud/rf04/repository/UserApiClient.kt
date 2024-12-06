package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.CurrentUser
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.RequestEntity
import org.springframework.stereotype.Component
import org.springframework.web.client.HttpClientErrorException
import org.springframework.web.client.RestTemplate

@Component
class UserApiClient(
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun validateToken(token: String): CurrentUser {
        val url = "${apiPropertiesConfig.user.baseUrl}/${apiPropertiesConfig.user.paths.validateToken}"

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .get(url)
            .headers(headers)
            .build()

        return try {
            return restTemplate.exchange(request, CurrentUser::class.java).body!!
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}