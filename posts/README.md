# Microservicio Posts

## Tabla de contenido

1. [Pre-requisitos](#pre-requisito-rutas)
2. [Estructura microservicio](#estructura-rutas)
   - [Archivos de soporte](#archivos-de-soporte)
   - [Carpeta main](#carpeta-main)
   - [Carpeta test](#carpeta-test)
3. [Ejecutar microservicio](#ejecutar-rutas)
   - [Instalar dependencias](#instalar-dependencias)
   - [Variables de entorno](#variables-de-entorno)
   - [Ejecutar aplicacion](#ejecutar-aplicacion)
   - [Ejecutar pruebas](#ejecutar-pruebas)
     - [Verificar coverage en pipeline](#cobertura-pipeline-rutas)
   - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
   - [Ejecutar Docker Compose](#ejecutar-docker-compose)
4. [Uso](#uso-rutas)
   - [Consumir la API](#consumir-la-api)
6. [Autor](#autor-rutas)

<a name="pre-requisito-rutas"></a>

### 1. Pre-requisitos

- Python 3.9 
- Pipenv 
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).

<a name="estructura-rutas"></a>

## 2. Estructura

Inicialmente la estructura de proyecto esta distribuida de la siguiente manera:

![Screenshot 2024-02-11 131544](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/baf26136-7564-4938-bd69-be6b99cfd296)

El microservicio utiliza Python y flask para ejecutar el servidor, y Pytest para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` el cual contiene la logica de la aplicación y 1 carpeta test `test` para ejecutar las pruebas unitarias, así como algunos archivos de soporte.


### Archivos de soporte

- `Pipfile`: archivo de configuración de nuestra aplicacion de Python el cual contiene las dependiencias necesarias para su correcto funcionamiento, por ejemplo flask, SQlalquemy, pytest, etc.
- `Pipfile.lock`: archivo de detalle de las dependencias, el cual se crea automaticamente cuando ejecuto el comando Pipenv install.
- `Dockerfile`: archivo de configuración de Docker para crear una imagen a partir de nuestra aplicación.
- `.env.template`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente "productivo".
- `.env.test`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente de pruebas.

### Carpeta main

- En la raiz de la carpeta '/src' tenemos el archivo main.py el cual contiene la la configuración inicial de la aplicación y al declaración de sus servicios controladores.

![main](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/2a9eaa56-7d8a-47ac-8db5-3ab5bbf00fec)

- En la carpeta '/blueprints' existe un archivo llamado actions.py el cual contiene cada uno de los servicios a exponer.
 
![bluprints](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/597542c9-0203-44ac-9a59-2f0c34cc77b2)

- En la carpeta '/validations' existe un archivo llamado validator.py el cual contiene las validaciones para cada servicio, como validar el token, validar los campos faltantes, formatos de campos, etc.

![validations](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/4dc6af9b-1c84-4e0f-856b-900c63389067)


- En la carpeta '/commands' existen archivos como create.py, delete.py, get.py, list.py y reset.py, los cuales contienen la logica de negocio y transaccionabilidad, como crear oferta, consultar ofertas, eliminar ofertas, etc.

![commands](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/52afbf6f-d81e-42c8-9a7a-4500f153854e)


- En la carpeta '/errors' tenemos un archivo llamado un archivo llamado errors.py el cual contiene todas las excepciones personalizadas las cuales estan creadas para devolver el codigo y mensaje solcitado en el enunciado.
![errors](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/86dfe585-34dc-4d29-ab25-876ae065aff7)


- En la carpeta '/models' tenemos un archivo llamado models.py el cual contiene la entidad Posts y schema asociado para la respectiva trasnformación a json.

![models](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/ec93ebab-ca26-4f3a-b536-36aacbad5fed)

### Carpeta test

- En la ruta test tenemos un archivo en la raiz llamado conftest.py, este archivo nos permite configurar que los test tomen las variables de entorno de el archivo .env.test, para que la base de datos levante con la base de datos de memoria

![tests](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/fe930523-fcf5-43d6-89ae-f15930c8e915)


## 3. Ejecutar microservicio

### Instalar dependencias

- Activamos el entorno virtual, ejecutando el comando .\venv\Scripts\Activate, cuando se active, podremos ver desde la consola (venv)

![activate](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/a51d73dc-4adb-4eee-af24-9ff2b48f02d4)

- En la carpeta raiz ejecutamos el comando 'pipenv install'

![install](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/aefa8f41-ac31-4d9f-8940-690ef4be28a6)


### Variables de entorno

Nuestra aplicación utiliza variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución, esas variables son:

- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

### Ejecutar aplicacion

Para ejecutar la aplicación nos situamos en la carpeta raíz del repositorio y ejecutamos 'docker compose up', ya que debemos consumir el microservicio de users:

![up](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/9d8bedcc-fb3d-4b10-bd8e-5a325bd0e237)

Al subir todo, nos debe salir así y podemos ver que podemos consumir nuestro microservicio por el puerto 3001

![running](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/1b267bf9-6394-404c-a78e-6d7978c11568)


### Ejecutar pruebas

Para ejecutar las pruebas unitarias del microservicios ejecuta el comando 'python -m pytest tests' desde la carpeta raíz del microservicio posts, en la consola podremos ver si las pruebas fueron exitosas:

![pytest](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/54720056-4f43-47a4-bafc-a0cedaf6c9db)

Tambien podemos ejecutar el comando 'pytest .\tests\blueprints\test_posts_operations.py --cov-fail-under=70 --cov=src --cov-report=html' si queremos evidenciar el porcentaje de cobertura, especificando que este debe ser mayor de 70%

![coverage](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/0b45448d-c62d-40b2-b9e6-74ec4bd5bd86)


<a name="cobertura-pipeline-rutas"></a>

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática cuando se realiza push a la rama main y generará un error cuando la cobertura
de código - coverage no supere el 70%.

![post1](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/607ac4b7-17ee-457d-a3ef-75a6a0a13fc6)

![post2](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/124221691/74d1e788-b77e-403f-83cd-96bd2f674b96)


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

<a name="uso-rutas"></a>

## 4. Uso

### Consumir la API
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega3/entrega3.json


<a name="autor-rutas"></a>

## 5. Autor
Victor Danilo Castañeda Pinzon - v.castanedap@uniandes.edu.co
