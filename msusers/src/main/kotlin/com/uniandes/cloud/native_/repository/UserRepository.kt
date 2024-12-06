package com.uniandes.cloud.native_.repository

import com.uniandes.cloud.native_.enums.UserStatus
import com.uniandes.cloud.native_.models.DefaultResponse
import com.uniandes.cloud.native_.models.User
import com.uniandes.cloud.native_.models.UserAfterCreate
import com.uniandes.cloud.native_.models.entities.UserEntity
import com.uniandes.cloud.native_.utils.generatePasswordHash
import com.uniandes.cloud.native_.utils.generateSalt
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.transactions.transaction
import org.springframework.stereotype.Repository
import java.time.LocalDateTime
import java.util.*

@Repository
class UserRepository : IUserRepository {
    override fun save(username: String, password: String, email: String, dni: String?, fullName: String?, phoneNumber: String?): UserAfterCreate {
        val id = UUID.randomUUID().toString()
        val salt = generateSalt()
        val securePassword = generatePasswordHash(password, salt)
        transaction {
            UserEntity.insert {
                it[this.id] = id
                it[this.username] = username
                it[this.password] = securePassword
                it[this.email] = email
                it[this.dni] = dni
                it[this.salt] = salt
                it[this.fullName] = fullName
                it[this.phoneNumber] = phoneNumber
            }
        }
        return UserAfterCreate(
                id,
                LocalDateTime.now()
        )
    }

    override fun findByUsername(username: String): Optional<User> {
        return Optional.ofNullable(
            transaction {
                UserEntity.selectAll()
                    .where(UserEntity.username eq username)
                    .map(ResultRow::toUser)
                    .firstOrNull()
            }
        )
    }

    override fun findByEmail(email: String): Optional<User> {
        return Optional.ofNullable(
                transaction {
                    UserEntity.selectAll()
                        .where(UserEntity.email eq email)
                        .map(ResultRow::toUser)
                        .firstOrNull()
                }
        )
    }

    override fun findById(id: String): Optional<User> {
        return Optional.ofNullable(
            transaction {
                UserEntity.selectAll()
                    .where(UserEntity.id eq id)
                    .map(ResultRow::toUser)
                    .firstOrNull()
            }
        )
    }

    override fun update(id: String, status: UserStatus?, dni: String?, fullName: String?, phoneNumber: String?): DefaultResponse {
        transaction {
            UserEntity.update ({ UserEntity.id eq id }) {
                it[UserEntity.status] = status
                it[UserEntity.dni] = dni
                it[UserEntity.fullName] = fullName
                it[UserEntity.phoneNumber] = phoneNumber
            }
        }
        return DefaultResponse(
            msg = "el usuario ha sido actualizado"
        )
    }

    override fun findByToken(token: String): Optional<User> {
        return Optional.ofNullable(
            transaction {
                UserEntity.selectAll()
                    .where(UserEntity.token eq token)
                    .andWhere { UserEntity.expireAt greaterEq LocalDateTime.now().withNano(0) }
                    .map(ResultRow::toUser)
                    .firstOrNull()
            }
        )
    }

    override fun resetTable() {
        transaction {
            UserEntity.deleteAll()
        }
    }

    override fun updateAuth(username: String, token: String, expireAt: LocalDateTime): Boolean {
        var success = 0
        transaction {
            success = UserEntity.update({ UserEntity.username eq username }) {
                it[this.token] = token
                it[this.expireAt] = expireAt
            }
        }
        return success > 0
    }

}

internal fun ResultRow.toUser() = User (
    id = this[UserEntity.id],
    username = this[UserEntity.username],
    email = this[UserEntity.email],
    password = this[UserEntity.password],
    dni = this[UserEntity.dni],
    fullName = this[UserEntity.fullName],
    phoneNumber = this[UserEntity.phoneNumber],
    salt = this[UserEntity.salt],
    status = this[UserEntity.status],
    createAt = this[UserEntity.createdAt],
    expireAt = this[UserEntity.expireAt],
    token = this[UserEntity.token]
)