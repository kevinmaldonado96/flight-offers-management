package com.uniandes.cloud.rf04.repository

import com.uniandes.cloud.rf04.config.props.ApiPropertiesConfig
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.OfferApiCallResponse
import com.uniandes.cloud.rf04.models.OfferApiClientRequestBody
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.RequestEntity
import org.springframework.stereotype.Component
import org.springframework.web.client.HttpClientErrorException
import org.springframework.web.client.RestTemplate

@Component
class OfferApiClient (
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun createOffer(offerApiClientRequestBody: OfferApiClientRequestBody, token: String): OfferApiCallResponse{
        val url = apiPropertiesConfig.offer.baseUrl

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .post(url)
            .headers(headers)
            .body(offerApiClientRequestBody)

        try {
            val response = restTemplate.exchange(request, OfferApiCallResponse::class.java).body!!
            return response
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}