import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import org.springframework.boot.gradle.tasks.bundling.BootJar

plugins {
	id("org.springframework.boot") version "3.2.2"
	id("io.spring.dependency-management") version "1.1.4"
	kotlin("jvm") version "1.9.22"
	kotlin("plugin.spring") version "1.9.22"
	jacoco
}

group = "com.uniandes.cloud"
version = "0.0.1-SNAPSHOT"

java {
	sourceCompatibility = JavaVersion.VERSION_17
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation("org.jetbrains.exposed:exposed-core:0.46.0")
	implementation("org.jetbrains.exposed:exposed-java-time:0.46.0")
	implementation("io.projectreactor:reactor-core:3.6.2")
	implementation("org.jetbrains.exposed:exposed-spring-boot-starter:0.46.0")
	implementation("org.postgresql:postgresql")
	testImplementation("com.ninja-squad:springmockk:3.1.2")

	testImplementation("org.junit.jupiter:junit-jupiter-api")

	testImplementation("org.jacoco:org.jacoco.agent:0.8.8")

	testImplementation("org.springframework.boot:spring-boot-starter-test") {
		exclude(group = "org.junit" )
		exclude(group = "org.junit.vintage" )
		exclude(group = "org.mockito" )
		exclude(group = "com.vaadin.external.google" )
	}
	testImplementation("com.h2database:h2:2.2.224")

}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs += "-Xjsr305=strict"
		jvmTarget = "17"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
	jacoco {
		isEnabled = true
	}
	systemProperty("spring.config.location", "classpath:/application-test.yml")
}

tasks.test {
	finalizedBy(tasks.jacocoTestReport) // Genera el reporte de cobertura después de las pruebas
}

tasks.jacocoTestReport {
	reports {
		xml.required = true // Habilita la generación de reportes XML
		html.required = true // Habilita la generación de reportes HTML
	}
}

tasks.withType<JacocoReport> {
	reports {
		xml.required = true
		html.required = true
	}

	afterEvaluate {
		val coverageParticipants = classDirectories.files
			.map { fileTree(it).exclude(
				"**/MsUserApplication.class",
				"**/config/*",
				"**/enums/*",
				"**/utils/*",
				"**/models/*",
			) }
			.let { files(it) }
		classDirectories.setFrom(coverageParticipants)
	}
}

tasks.getByName<BootJar>("bootJar") {
	archiveFileName.set("msusers.jar")
}

jacoco {
	toolVersion = "0.8.8"
}

tasks.jacocoTestCoverageVerification {
	violationRules {
		rule {
			limit {
				minimum = BigDecimal(0.7)
			}
		}
	}
}