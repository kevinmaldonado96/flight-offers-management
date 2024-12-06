package com.uniandes.cloud.native_.models.entities

import com.uniandes.cloud.native_.enums.UserStatus
import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.javatime.datetime
import java.time.LocalDateTime

object UserEntity : Table("users") {
    val id = varchar("id", 100)
    val username = varchar("username", 100).uniqueIndex()
    val email = varchar("email", 100).uniqueIndex()
    val phoneNumber = varchar("phoneNumber", 100).nullable()
    val dni = varchar("dni", 100).nullable()
    val fullName = varchar("fullName", 100).nullable()
    val password = varchar("password", 100)
    val salt = binary("salt", 100)
    val token = varchar("token", 100).nullable()
    val status = enumerationByName("status", 50, UserStatus::class).nullable()
    val expireAt = datetime("expireAt").nullable()
    val createdAt = datetime("createdAt").default(LocalDateTime.now().withNano(0))
    val updateAt = datetime("updateAt").clientDefault { LocalDateTime.now().withNano(0) }

    override val primaryKey = PrimaryKey(id)
}
