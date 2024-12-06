package com.uniandes.cloud.native_.config


import org.jetbrains.exposed.spring.autoconfigure.ExposedAutoConfiguration
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.DatabaseConfig
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.autoconfigure.ImportAutoConfiguration
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean
import org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Profile
import javax.sql.DataSource

@Configuration
@ImportAutoConfiguration(
        value = [ExposedAutoConfiguration::class],
        exclude = [DataSourceTransactionManagerAutoConfiguration::class]
)
@Profile("prd")
class ExposedConfiguration(
        @Autowired private val dataSource: DataSource
) {

    @Bean
    fun databaseConfig() = DatabaseConfig {
        useNestedTransactions = true
    }

    @Bean
    fun database(datasource: DataSource): Database {
        return Database.connect(dataSource)
    }

    @Bean
    @ConditionalOnMissingBean
    fun databaseInitializer(): DbInitializer {
        return DbInitializer()
    }
}