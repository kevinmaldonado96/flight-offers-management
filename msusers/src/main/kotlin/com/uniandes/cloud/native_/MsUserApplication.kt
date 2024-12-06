package com.uniandes.cloud.native_

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication()
class MsUserApplication

fun main(args: Array<String>) {
	runApplication<MsUserApplication>(*args)
}
