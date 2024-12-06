package com.uniandes.cloud.native_.test_database

import com.uniandes.cloud.native_.models.entities.UserEntity
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.StdOutSqlLogger
import org.jetbrains.exposed.sql.addLogger
import org.jetbrains.exposed.sql.transactions.transaction
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Primary
import org.springframework.jdbc.datasource.DriverManagerDataSource
import javax.sql.DataSource

@TestConfiguration
class DatabaseConfig {

    @Bean
    @Primary
    fun datasource(): DataSource {
        return DriverManagerDataSource().apply {
            setDriverClassName("org.h2.Driver")
            url = "jdbc:h2:mem:db_test;DB_CLOSE_DELAY=-1"
        }
    }

    @Bean
    fun initDatabase(dataSource: DataSource) {
        val db = Database.connect(dataSource)

        transaction(db) {
            addLogger(StdOutSqlLogger)
            SchemaUtils.create(UserEntity)
        }
    }

}