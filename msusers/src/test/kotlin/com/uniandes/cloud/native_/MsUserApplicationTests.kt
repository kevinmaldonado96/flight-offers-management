package com.uniandes.cloud.native_

import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.context.annotation.Profile

@SpringBootTest
@Profile("test")
class MsUserApplicationTests {

	@Test
	fun contextLoads() {
	}

}
