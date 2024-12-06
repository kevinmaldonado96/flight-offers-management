package com.uniandes.cloud.native_.test_database

import com.uniandes.cloud.native_.models.entities.UserEntity
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction

fun deleteAllTestData() {
    transaction {
        UserEntity.deleteAll()
    }
}