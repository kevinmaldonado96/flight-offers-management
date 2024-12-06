package com.uniandes.cloud.native_.controller

import com.uniandes.cloud.native_.exceptions.HeaderNotFoundException
import com.uniandes.cloud.native_.exceptions.UnauthorizedException
import com.uniandes.cloud.native_.models.*
import com.uniandes.cloud.native_.service.UserService
import com.uniandes.cloud.native_.utils.validateToken
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PatchMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/users")
class UserController(
        private val userService: UserService
) {

    @PostMapping
    fun create(@RequestBody user: UserCreateRequestBody): ResponseEntity<UserAfterCreate> {
        val response = userService.save(
                username = user.username,
                password = user.password,
                email = user.email,
                dni = user.dni,
                fullName = user.fullName,
                phoneNumber = user.phoneNumber
        )
        return ResponseEntity(response, HttpStatus.CREATED)
    }

    @PatchMapping("/{id}")
    fun update(@PathVariable("id") id: String, @RequestBody request: UserUpdateRequestBody): ResponseEntity<DefaultResponse> {
        if (!request.hasAttributesNotNull())
            return ResponseEntity.badRequest().build()
        val response = userService.update(
            id,
            request.status,
            request.dni,
            request.fullName,
            request.phoneNumber
        )
        return ResponseEntity(response, HttpStatus.OK)
    }

    @PostMapping("/auth")
    fun login(@RequestBody credentials: Credentials): ResponseEntity<Session>{
        val response = userService.login(credentials.username, credentials.password)
        return ResponseEntity.ok(response)
    }

    @GetMapping("/me")
    fun findByToken(@RequestHeader("Authorization") token: String?): ResponseEntity<CurrentUser> {
        if(token.isNullOrEmpty())
            throw HeaderNotFoundException()

        val validToken = validateToken(token) ?: throw UnauthorizedException()

        val response = userService.currentUser(validToken)
        return ResponseEntity.ok(response)

    }

    @GetMapping("/ping")
    fun ping() : ResponseEntity<String> {
        return ResponseEntity("pong", HttpStatus.OK)
    }

    @PostMapping("/reset")
    fun reset(): ResponseEntity<DefaultResponse>{
        userService.resetData()
        return ResponseEntity(DefaultResponse("Todos los datos fueron eliminados"),
            HttpStatus.OK)
    }
}