package com.uniandes.cloud.rf04.config.props

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.boot.context.properties.bind.ConstructorBinding

@ConfigurationProperties(prefix = "api")
data class ApiPropertiesConfig @ConstructorBinding constructor(
    val user: User,
    val post: Post,
    val offer: Offer
) {

    data class User(
        val baseUrl: String,
        val paths: UserPath
    )

    data class UserPath(
        val validateToken: String
    )

    data class Post(
        val baseUrl: String,
        val paths: PostPaths
    )

    data class PostPaths(
        val findById: String
    )

    data class Offer(
        val baseUrl: String
    )
}