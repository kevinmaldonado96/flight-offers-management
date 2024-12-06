package com.uniandes.cloud.rf04.controller

import com.uniandes.cloud.rf04.exceptions.HeaderNotFoundException
import com.uniandes.cloud.rf04.exceptions.UnauthorizedException
import com.uniandes.cloud.rf04.models.OfferApiResponse
import com.uniandes.cloud.rf04.models.OfferRequestBody
import com.uniandes.cloud.rf04.models.toOffer
import com.uniandes.cloud.rf04.service.OfferService
import com.uniandes.cloud.rf04.utils.validateToken
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/rf004/posts")
class OfferController (
    private val offerService: OfferService
) {

    @PostMapping("/{postId}/offers")
    fun createOffer(@RequestHeader("Authorization") token: String?, @PathVariable postId: String, @RequestBody body: OfferRequestBody): ResponseEntity<OfferApiResponse> {
        if(token.isNullOrEmpty())
            throw HeaderNotFoundException()

        val validToken = validateToken(token) ?: throw UnauthorizedException()

        val response = offerService.createPost(postId, body.toOffer(), validToken)
        return ResponseEntity(response, HttpStatus.CREATED)
    }

    @PostMapping("/ping")
    fun ping(): ResponseEntity<String> {
        return ResponseEntity("pong", HttpStatus.OK)
    }
}