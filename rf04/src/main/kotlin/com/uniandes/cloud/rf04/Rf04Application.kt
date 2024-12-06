package com.uniandes.cloud.rf04

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.ConfigurationPropertiesScan
import org.springframework.boot.runApplication

@SpringBootApplication
@ConfigurationPropertiesScan
class Rf04Application

fun main(args: Array<String>) {
	runApplication<Rf04Application>(*args)
}
