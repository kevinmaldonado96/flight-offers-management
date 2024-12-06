package com.uniandes.cloud.native_.config

import com.uniandes.cloud.native_.models.entities.UserEntity
import jakarta.annotation.PostConstruct
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Component
import javax.sql.DataSource

@Component
class DbInitializer {

    @Autowired
    lateinit var dataSource: DataSource

    @PostConstruct
    fun initialize() {
        try {
            Database.connect(dataSource)
            transaction {
                SchemaUtils.create(UserEntity)
            }
        }catch (ex: Exception){
            ex.printStackTrace()
        }
    }
}