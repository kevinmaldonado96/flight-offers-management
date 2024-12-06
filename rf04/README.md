# Microservicio RF004
Este microservicio permite crear oferta integrándose con los servicios de ofertas y usuarios.

## Tabla de contenido

1. [Pre-requisitos](#1-pre-requisitos)
2. [Estructura](#2-estructura)
    - [Archivos de soporte](#archivos-de-soporte)
    - [Carpeta main](#carpeta-main)
    - [Carpeta test](#carpeta-test)

3. [Ejecutar microservicio](#3-ejecutar-microservicio)
    - [Instalar dependencias](#instalar-dependencias)
    - [Variables de entorno](#variables-de-entorno)
    - [Ejecutar el servidor](#ejecutar-el-servidor)
    - [Ejecutar pruebas](#ejecutar-pruebas)
        - [Verificar coverage en pipeline](#cobertura-pipeline-usuarios)

    - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
    - [Ejecutar Docker Compose](#ejecutar-docker-compose)

4. [Uso](#4-uso)
    - [Consumir la API](#consumir-la-api)

5. [Otras caracteristicas](#5-otras-caracteristicas)
6. [Autor](#6-autor)

### 1. Pre-requisitos

- openjdk 17:Temurin
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://adoptium.net/temurin/releases/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

## 2. Estructura

```
.
├── rf04
│   ├── src
│   │   ├── main
│   │   │   └── kotlin
│   │   │   │	└── com
│   │   │   │	│	└── uniandes
│   │   │   │	│	│	└── cloud
│   │   │   │	│	│	│	└── rf04
│   │   │   │	│	│	│	│	└── config
|   |   |   |   |   |   |   |   |   └── props
|   |   |   |   |   |   |   |   |   |   └── ApiPropertiesConfig.kt
│   │   │   │	│	│	│	│	│	└── AppConfig.kt.java
│   │   │   │	│	│	│	│	└── controller
│   │   │   │	│	│	│	│	│	└── OfferController.java
│   │   │   │	│	│	│	│	└── enums
│   │   │   │	│	│	│	│	│	└── enums.kt
│   │   │   │	│	│	│	│	└── exceptions
│   │   │   │	│	│	│	│	│	└── exceptions.kt
│   │   │   │	│	│	│	│	│	└── GlobalErrorHandlerException.kt
│   │   │   │	│	│	│	│	└── models
│   │   │   │	│	│	│	│	│	└── Offer.kt
│   │   │   │	│	│	│	│	│	└── Post.kt
│   │   │   │	│	│	│	│	│	└── User.kt
│   │   │   │	│	│	│	│	└── repository
│   │   │   │	│	│	│	│	│	└── OfferApiClient.kt
│   │   │   │	│	│	│	│	│	└── UserApiClient.kt
│   │   │   │	│	│	│	│	│	└── PostsApiClient.kt
│   │   │   │	│	│	│	│	└── service
│   │   │   │	│	│	│	│	│	└── OfferService.java
│   │   │   │	│	│	│	│	└── utils
│   │   │   │	│	│	│	│	│	└── Utils.kt
│   │   │   │	│	│	│	│	└── Rf04Application.kt
│   │   │   │	└── resources
│   │   │   │	│	└── application.yml
│   │   ├── test
│   │   │   └── kotlin
│   │   │   │	└── com
│   │   │   │	│	└── uniandes
│   │   │   │	│	│	└── cloud
│   │   │   │	│	│	│	└── rf04
│   │   │   │	│	│	│	│	└── controller
│   │   │   │	│	│	│	│	│	└── OfferControllerTest.java
│   │   │   │	│	│	│	│	└── exceptions
│   │   │   │	│	│	│	│	│	└── GlobalErrorHandlerExceptionTest.kt
│   │   │   │	│	│	│	│	└── repository
│   │   │   │	│	│	│	│	│	└── OfferApiClientTest.kt
│   │   │   │	│	│	│	│	│	└── UserApiClientTest.kt
│   │   │   │	│	│	│	│	│	└── PostsApiClientTest.kt
│   │   │   │	│	│	│	│	└── service
│   │   │   │	│	│	│	│	│	└── OfferServiceTest.java
│   │   │   │	│	│	│	│	└── Rf04ApplicationTests.kt.java
│   │   │   │	└── resources
│   │   │   │	│	└── application-test.yml
│   ├── build.gradle.kts
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── gradlew
│   ├── gradlew.bat
```


El microservicio utiliza java y spring boot para ejecutar el servidor, y jacoco para ejecutar las pruebas unitarias.
Dentro de este hay 1 carpeta principal `src` y esta a su vez contiene 2 carpetas que separan la lógica de negocio `main` de las pruebas `test`, así como algunos archivos de soporte.

### Archivos de soporte

- `build.gradle.kts`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. Consulta la sección **Instalar dependencias**.
- `gradlew`: Es un script de shell que permite ejecutar Gradle sin necesidad de tener Gradle instalado previamente en el sistema..
- `gradlew.bat`: Permite ejecutar tareas de Gradle sin necesidad de tener Gradle instalado previamente en el sistema.
- `settings.gradlew.kts`: Se utiliza para configurar la estructura del proyecto y personalizar la configuración de Gradle.
- `Dockerfile`: Definición para construir la imagen Docker del microservicio. Consulta la sección **Ejecutar desde Dockerfile**.
- `docker-compose`: herramienta que se utiliza para definir y gestionar aplicaciones Docker multi-contenedor.

### Carpeta main

Esta carpeta contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio, 
así como para la comunicación con la base de datos. Las carpetas de la lógica se encuentra en el path `/kotlin/com/uniandes/cloud/rf04`, 
dentro de este hay 6 carpetas principales: `config`, `controller`, `models`, `repository`, `service`, `exceptions`.

- `/config`: Esta carpeta contiene las clases de configuración inicial, las cuales se cargan del archivo de propiedades
de la aplicación y la clase de configuración que agrega como un componente nativo del framework el objeto que hará las peticiones rest.

```kotlin
//ApiPropertiesConfig.kt
@ConfigurationProperties(prefix = "api")
data class ApiPropertiesConfig @ConstructorBinding constructor(
    val user: User,
    val post: Post,
    val offer: Offer
) {

    data class User(
        val baseUrl: String,
        val paths: UserPath
    )

    data class UserPath(
        val validateToken: String
    )

    data class Post(
        val baseUrl: String,
        val paths: PostPaths
    )

    data class PostPaths(
        val findById: String
    )

    data class Offer(
        val baseUrl: String
    )
}

//AppConfig.kt
@Configuration
class AppConfig {

    @Bean
    fun restTemplate() = RestTemplate()

}
```

- `Controller`: Esta carpeta contiene un archivo llamado `OfferController`, este es el que disponibiliza el entrypoint para ser consumidos por los clientes.

```kotlin
//OfferController.kt
@RestController
@RequestMapping("/rf004/posts")
class OfferController (
    private val offerService: OfferService
) {

    @PostMapping("/{postId}/offers")
    fun createOffer(@RequestHeader("Authorization") token: String?, @PathVariable postId: String, @RequestBody body: OfferRequestBody): ResponseEntity<OfferApiResponse> {
        if(token.isNullOrEmpty())
            throw HeaderNotFoundException()

        val validToken = validateToken(token) ?: throw UnauthorizedException()

        val response = offerService.createPost(postId, body.toOffer(), validToken)
        return ResponseEntity(response, HttpStatus.CREATED)
    }

    @PostMapping("/ping")
    fun ping(): ResponseEntity<String> {
        return ResponseEntity("pong", HttpStatus.OK)
    }
}
```

- `models`:  Esta carpeta contiene las clases que representan un objeto en el ecosistema 

- `Repositories`: Esta carpeta contiene los archivos `UserApiClient`, `OfferApiClient` y `PostsApiClient` que es el que permite operar sobre la base de datos.
```kotlin
//UserApiClient.kt
@Component
class UserApiClient(
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun validateToken(token: String): CurrentUser {
        val url = "${apiPropertiesConfig.user.baseUrl}/${apiPropertiesConfig.user.paths.validateToken}"

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .get(url)
            .headers(headers)
            .build()

        return try {
            return restTemplate.exchange(request, CurrentUser::class.java).body!!
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}

//OfferApiClient.kt
@Component
class OfferApiClient (
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun createOffer(offerApiClientRequestBody: OfferApiClientRequestBody, token: String): OfferApiCallResponse{
        val url = apiPropertiesConfig.offer.baseUrl

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .post(url)
            .headers(headers)
            .body(offerApiClientRequestBody)

        try {
            val response = restTemplate.exchange(request, OfferApiCallResponse::class.java).body!!
            return response
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}

//PostsApiClient.kt
@Component
class PostsApiClient(
    private val restTemplate: RestTemplate,
    private val apiPropertiesConfig: ApiPropertiesConfig
) {

    fun findOfferById(postId: String, token: String): PostApiCallResponse {

        val url = "${apiPropertiesConfig.post.baseUrl}/${apiPropertiesConfig.post.paths.findById.replace("#{post_id}", postId)}"

        val headers = HttpHeaders()
        headers.contentType = MediaType.APPLICATION_JSON
        headers.set("Authorization", token)

        val request = RequestEntity
            .get(url)
            .headers(headers)
            .build()

        try {
            val response = restTemplate.exchange(request, PostApiCallResponse::class.java).body!!
            return response
        }catch (ex: HttpClientErrorException) {
            when (ex.statusCode){
                HttpStatus.UNAUTHORIZED -> throw UnauthorizedException()
                HttpStatus.NOT_FOUND -> throw PostNotFoundException()
                else -> throw Exception("Error with few information")
            }
        }
    }
}
```

- `exceptions`: Permite lanzar excepciones controladas a través de la respuesta de la API. Esta contiene 2 archivos `Exceptions` que son las definiciones de las excepciones y `GlobalErrorHandlerException` que es la manera en que va a responder la api ante estas excepciones.
```kotlin
//Exceptions.kt
class HeaderNotFoundException() : RuntimeException()
class UnauthorizedException() : RuntimeException()
class PostNotFoundException() : RuntimeException()
class PostAlreadyExistForUser() : RuntimeException()
class PostExpiredException() : RuntimeException()

//GlobalErrorHandlerException.kt
@ControllerAdvice
class GlobalErrorHandlerException {

    @ExceptionHandler(HeaderNotFoundException::class)
    fun handleError(ex: HeaderNotFoundException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.FORBIDDEN)
    }

    @ExceptionHandler(UnauthorizedException::class)
    fun handleError(ex: UnauthorizedException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.UNAUTHORIZED)
    }

    @ExceptionHandler(PostNotFoundException::class)
    fun handleError(ex: PostNotFoundException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(PostAlreadyExistForUser::class)
    fun handleError(ex: PostAlreadyExistForUser): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
    }

    @ExceptionHandler(PostExpiredException::class)
    fun handleError(ex: PostExpiredException): ResponseEntity<RequestFailure> {
        return handleError(HttpStatus.PRECONDITION_FAILED)
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
```

### Carpeta test

Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/main`

## 3. Ejecutar microservicio

### Instalar dependencias
Ubicándonos en la raíz del proyecto del microservicio ejectuar el comando:

```bash
$> ./gradlew dependencies
```

### Variables de entorno

El servidor Spring utiliza variables de entorno para configurar los paths de los microservicios con los que este debe interactuar, 
estas variables son:

- USERS_PATH: Path del microservicio de usuarios
- POSTS_PATH: Path del microservicio de publicaciones
- OFFERS_PATH: Path del microservicio de ofertas

Estas variables de entorno deben especificarse en el archivo properties de la aplicación en el perfil que actuará como productivo `/src/main/resources/application.yml`

```ini
.
├── rf04
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

2- Luego hay que navegar hasta el path `rf04/build/libs` y ejecutar el comando

```ini
.
├── rf04
│   ├── build
│   │   ├── libs
│   │   │   └── rf04.java
```

```bash
$> java -jar rf04/build/libs/rf04.jar
```

### Ejecutar pruebas

Para ejecutar las pruebas unitarias del microservicios ejecuta el siguiente comando desde la carpeta raíz del microservicio `rf04`:

```bash
$> ./gradlew build jacocoTestReport
```

para visualizar el reporte debe ejecutar el archivo index.html generado por el comando.

```ini 
.
├── rf04
│   ├── build
│   │   ├── reports
│   │   │   └── jacoco
│   │   │   │	└── test
│   │   │   │	│	└── html
│   │   │   │	│	│	└── index.html
```

Si quiere validar si el coverage supera el 70% de cobertura de código, después de haber ejecutado el comando anterior ejecute el siguiente:

```bash 
 $> ./gradlew jacocoTestCoverageVerification
```

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática y generará un error cuando la cobertura
de código - coverage no supere el 70%.

Pruebas y coverage satisfactorios
![coverage_success.png](docs%2Fgithub%2Fcoverage_success.png)

Error de coverage
![coverage_error.png](docs%2Fgithub%2Fcoverage_error.png)

Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:

```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```

Y para ejecutar esta imagen construida, utiliza el siguiente comando:

```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecutar Docker Compose

Para ejecutar todos los microservicios al mismo tiempo utilizamos docker-compose, mediante este se declara y configura cada Dockerfile de los microservicios. Para ejecutar docker-compose, 
debe estar situado por fuera de los microservicios y ejecutar el siguiente comando:

```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

# 4. Uso

### Consumir la API

Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:

- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega3/entrega3.json

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

## 5. Otras caracteristicas

No hay.

## 6. Autor

Jorge Andrés Romero Gutiérrez -`ja.romerog12@uniandes.edu.co`