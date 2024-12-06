# Microservicio de usuarios
## Tabla de contenido

1. [Pre-requisitos](#pre-requisito-usuarios)
2. [Estructura microservicio](#estructura-usuarios)
    - [Archivos de soporte](#archivos-de-soporte)
    - [Carpeta main](#carpeta-main)
    - [Carpeta test](#carpeta-test)
3. [Ejecutar microservicio](#ejecutar-usuarios)
    - [Instalar dependencias](#instalar-dependencias)
    - [Variables de entorno](#variables-de-entorno)
    - [Ejecutar el servidor](#ejecutar-el-servidor)
    - [Ejecutar pruebas](#ejecutar-pruebas)
      - [Verificar coverage en pipeline](#cobertura-pipeline-usuarios)
    - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
    - [Ejecutar Docker Compose](#ejecutar-docker-compose)
4. [Uso](#uso-usuarios)
    - [Consumir la API](#consumir-la-api)
5. [Otras características](#otras-caracteristicas-usuarios)
6. [Autor](#autor-usuarios)

<a name="pre-requisito-usuarios"></a>
### 1. Pre-requisitos

- openjdk 17:Temurin
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://adoptium.net/temurin/releases/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

<a name="estructura-usuarios"></a>
## 2. Estructura

Estructura del proyecto
```
.
├── msusers
│   ├── src
│   │   ├── main
│   │   │   └── kotlin
│   │   │   │	└── com
│   │   │   │	│	└── uniandes
│   │   │   │	│	│	└── cloud
│   │   │   │	│	│	│	└── native_
│   │   │   │	│	│	│	│	└── config
│   │   │   │	│	│	│	│	│	└── DbInitializer.java
│   │   │   │	│	│	│	│	│	└── ExposedConfiguration.java
│   │   │   │	│	│	│	│	└── controller
│   │   │   │	│	│	│	│	│	└── UserController.java
│   │   │   │	│	│	│	│	└── enums
│   │   │   │	│	│	│	│	│	└── enums.kt
│   │   │   │	│	│	│	│	└── exceptions
│   │   │   │	│	│	│	│	│	└── exceptions.kt
│   │   │   │	│	│	│	│	│	└── GlobalErrorHandlerException.kt
│   │   │   │	│	│	│	│	└── models
│   │   │   │	│	│	│	│	│	└── entities
│   │   │   │	│	│	│	│	│	│	└── UserEntity.kt
│   │   │   │	│	│	│	│	│	└── Auth.kt
│   │   │   │	│	│	│	│	│	└── DefaultResponse.kt
│   │   │   │	│	│	│	│	│	└── User.kt
│   │   │   │	│	│	│	│	└── repository
│   │   │   │	│	│	│	│	│	└── interfaces.kt
│   │   │   │	│	│	│	│	│	└── UserRepository.kt
│   │   │   │	│	│	│	│	└── service
│   │   │   │	│	│	│	│	│	└── UserService.java
│   │   │   │	│	│	│	│	└── utils
│   │   │   │	│	│	│	│	│	└── Utils.kt
│   │   │   │	│	│	│	│	└── MsUserApplication.kt.java
│   │   │   │	└── resources
│   │   │   │	│	└── application.yml
│   │   ├── test
│   │   │   └── kotlin
│   │   │   │	└── com
│   │   │   │	│	└── uniandes
│   │   │   │	│	│	└── cloud
│   │   │   │	│	│	│	└── native_
│   │   │   │	│	│	│	│	└── controller
│   │   │   │	│	│	│	│	│	└── UserControllerTest.java
│   │   │   │	│	│	│	│	└── exceptions
│   │   │   │	│	│	│	│	│	└── GlobalErrorHandlerExceptionTest.kt
│   │   │   │	│	│	│	│	└── repository
│   │   │   │	│	│	│	│	│	└── UserRepositoryTest.kt
│   │   │   │	│	│	│	│	└── service
│   │   │   │	│	│	│	│	│	└── UserServiceTest.java
│   │   │   │	│	│	│	│	└── test_database
│   │   │   │	│	│	│	│	│	└── DatabaseConfig.java
│   │   │   │	│	│	│	│	│	└── DatabaseActions.java
│   │   │   │	│	│	│	│	└── MsUserApplicationTests.kt.java
│   │   │   │	└── resources
│   │   │   │	│	└── application-test.yml
│   ├── build.gradle.kts
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── gradlew
│   ├── gradlew.bat
│   ├── HELP.md
│   ├── settings.gradle.kts
```


El microservicio utiliza java y spring boot para ejecutar el servidor, y jacoco para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` y esta a su vez contiene 2 carpetas que separan la lógica de negocio `main` de las pruebas `test`, así como algunos archivos de soporte.

### Archivos de soporte
- `build.gradle.kts`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. Consulta la sección **Instalar dependencias**.
- `gradlew`: Es un script de shell que permite ejecutar Gradle sin necesidad de tener Gradle instalado previamente en el sistema..
- `gradlew.bat`: Permite ejecutar tareas de Gradle sin necesidad de tener Gradle instalado previamente en el sistema.
- `settings.gradlew.kts`: Se utiliza para configurar la estructura del proyecto y personalizar la configuración de Gradle.
- `Dockerfile`: Definición para construir la imagen Docker del microservicio. Consulta la sección **Ejecutar desde Dockerfile**.
- `docker-compose`: herramienta que se utiliza para definir y gestionar aplicaciones Docker multi-contenedor.

### Carpeta main
Esta carpeta contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio, así como para la comunicación con la base de datos. Las carpetas de la lógica se encuentra en el path `/kotlin/com/uniandes/cloud/native_`, dentro de este hay 6 carpetas principales: `config`, `controller`, `models`, `repository`, `service`, `exceptions`.

- `/config`: Esta carpeta contiene las clases que permiten la cconexión con la base de datos, `DbInitializer` contiene la construcción del datasource al momento que la aplicación sube y el archivo `ExposedConfiguration` que es el que disponibiliza el datasource a través de la aplicación.

```kotlin
//config/DbInitializer.kt
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

//config/ExposedConfiguration.kt
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

```

- `Controller`: Esta carpeta contiene un archivo llamado `UserController`, este es el que disponibiliza los entrypoints para ser consumidos por los clientes.

```kotlin
//UserController.kt
import com.uniandes.cloud.native_.exceptions.HeaderNotFoundException
import com.uniandes.cloud.native_.exceptions.UnauthorizedException
import com.uniandes.cloud.native_.models.*
import com.uniandes.cloud.native_.service.UserService
import com.uniandes.cloud.native_.utils.validateToken
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PatchMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/users")
class UserController(
        private val userService: UserService
) {

    @PostMapping
    fun create(@RequestBody user: UserCreateRequestBody): ResponseEntity<UserAfterCreate> {
        val response = userService.save(
                username = user.username,
                password = user.password,
                email = user.email,
                dni = user.dni,
                fullName = user.fullName,
                phoneNumber = user.phoneNumber
        )
        return ResponseEntity(response, HttpStatus.CREATED)
    }

    @PatchMapping("/{id}")
    fun update(@PathVariable("id") id: String, @RequestBody request: UserUpdateRequestBody): ResponseEntity<DefaultResponse> {
        if (!request.hasAttributesNotNull())
            return ResponseEntity.badRequest().build()
        val response = userService.update(
            id,
            request.status,
            request.dni,
            request.fullName,
            request.phoneNumber
        )
        return ResponseEntity(response, HttpStatus.OK)
    }

    @PostMapping("/auth")
    fun login(@RequestBody credentials: Credentials): ResponseEntity<Session>{
        val response = userService.login(credentials.username, credentials.password)
        return ResponseEntity.ok(response)
    }

    @GetMapping("/me")
    fun findByToken(@RequestHeader("Authorization") token: String?): ResponseEntity<CurrentUser> {
        if(token.isNullOrEmpty())
            throw HeaderNotFoundException()

        val validToken = validateToken(token) ?: throw UnauthorizedException()

        val response = userService.currentUser(validToken)
        return ResponseEntity.ok(response)

    }

    @GetMapping("/ping")
    fun ping() : ResponseEntity<String> {
        return ResponseEntity("pong", HttpStatus.OK)
    }

    @PostMapping("/reset")
    fun reset(): ResponseEntity<DefaultResponse>{
        userService.resetData()
        return ResponseEntity(DefaultResponse("Todos los datos fueron eliminados"),
            HttpStatus.OK)
    }
}

```

- `models`:  Esta carpeta contiene la capa de persistencia y los modelos de respuesta de la api. Dentro de esta hay una carpeta llamada `entities` que contiene un archivo `UserEntity` que representa una tabla de la base de datos como un modelo.

```kotlin
//UserEntitity.kt
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
```

- `Repositories`: Esta carpeta contiene un archivo `UserRepository` que es el que permite operar sobre la base de datos.

```kotlin
//UserRepository.kt

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

```

- `exceptions`: Permite lanzar excepciones controladas a través de la respuesta de la API. Esta contiene 2 archivos `Exceptions` que son las definiciones de las excepciones y `GlobalErrorHandlerException` que es la manera en que va a responder la api ante estas excepciones.

```kotlin
//Exceptions.kt
class HeaderNotFoundException() : RuntimeException()
class UsernameWithWhiteSpacesCharactersException() : RuntimeException()
class InvalidEmailFormatException() : RuntimeException()
class RecordAlreadyExistException() : RuntimeException()
class UserDoesNotExistException() : RuntimeException()
class InvalidUsernameOrPasswordException() : RuntimeException()
class UnauthorizedException() : RuntimeException()

//GlobalErrorHandlerException
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler

@ControllerAdvice
class GlobalErrorHandlerException {

    @ExceptionHandler(HeaderNotFoundException::class)
    fun handleError(ex: HeaderNotFoundException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.FORBIDDEN)
    }

    @ExceptionHandler(UsernameWithWhiteSpacesCharactersException::class)
    fun handleError(ex: UsernameWithWhiteSpacesCharactersException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(InvalidEmailFormatException::class)
    fun handleError(ex: InvalidEmailFormatException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(RecordAlreadyExistException::class)
    fun handleError(ex: RecordAlreadyExistException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
    }

    @ExceptionHandler(UserDoesNotExistException::class)
    fun handleError(ex: UserDoesNotExistException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(InvalidUsernameOrPasswordException::class)
    fun handleError(ex: InvalidUsernameOrPasswordException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(UnauthorizedException::class)
    fun handleError(ex: UnauthorizedException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.UNAUTHORIZED)
    }

    fun handleError(
        responseStatus: HttpStatus,
    ): ResponseEntity<RequestFailure> {
        return ResponseEntity(
            RequestFailure(responseStatus.value()),
            responseStatus
        )
    }
}
data class RequestFailure(val status: Int)
```

### Carpeta test
Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/main`

<a name="ejecutar-usuarios"></a>
## 3. Ejecutar microservicio

### Instalar dependencias
Ubicándonos en la raíz del proyecto del microservicio ejectuar el comando:

```bash
$> ./gradlew dependencies
``` 
```agsl
.
├── msusers
```

### Variables de entorno

El servidor Spring utiliza variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución. A alto nivel, esas variables son:
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

Estas variables de entorno deben especificarse en el archivo properties de la aplicación en el perfil que actuará como productivo `/src/main/resources/application.yml`
```
.
├── msusers
│   ├── src
│   │   ├── main
│   │   │   └── resources
│   │   │   │	└── application.yml
```

### Ejecutar el servidor
Una vez que las variables de entorno estén configuradas correctamente, para ejecutar el servidor se deben utilizar 2 comandos:
1- Este comando compilará tu aplicación Spring Boot y generará los artefactos de construcción, como el archivo JAR o WAR, en el directorio build/libs de tu proyecto.
```bash
$> ./gradlew build
```
2- Luego hay que navegar hasta el path `msusers/build/libs` y ejecutar el comando
```
.
├── msusers
│   ├── build
│   │   ├── libs
│   │   │   └── msusers.java
```

```bash
$> java -jar msusers/build/libs/msusers.jar.jar
```

### Ejecutar pruebas
Para ejecutar las pruebas unitarias del microservicios ejecuta el siguiente comando desde la carpeta raíz del microservicio `msusers`:
```bash
$> ./gradlew build jacocoTestReport
```
para visualizar el reporte debe ejecutar el archivo index.html generado por el comando.
```
.
├── msusers
│   ├── build
│   │   ├── reports
│   │   │   └── jacoco
│   │   │   │	└── test
│   │   │   │	│	└── html
│   │   │   │	│	│	└── index.html
```

Si quiere validar si el coverage supera el 70% de cobertura de código, después de haber ejecutado el comando anterior ejecute el siguiente: <br/>
```bash
 $> ./gradlew jacocoTestCoverageVerification
```

<a name="cobertura-pipeline-usuarios"></a>
### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática y generará un error cuando la cobertura
de código - coverage no supere el 70%.

Pruebas y coverage satisfactorios
![coverage_success.png](docs%2Fgithub%2Fcoverage_success.png)

Error de coverage
![coverage_error.png](docs%2Fgithub%2Fcoverage_error.png)


### Ejecutar desde Dockerfile
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:
```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecutar Docker Compose
Para ejecutar todos los microservicios al mismo tiempo, utilizamos docker-compose para declarar y configurar cada Dockerfile de los microservicios. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

<a name="uso-usuarios"></a>
## 4. Uso 

### Consumir la API
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega3/entrega3.json

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

<a name="otras-caracteristicas-usuarios"></a>
## 5. Otras caractrísticas
No hay.

<a name="autor-usuarios"></a>
## 6. Autor
Jorge Andrés Romero Gutiérrez -`ja.romerog12@uniandes.edu.co`
