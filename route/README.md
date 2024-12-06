# microservicio Route

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
5. [Autor](#autor-rutas)

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

Inicialmente la estructura de proyecto esta distribuida de la siguiente manera

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/1265e97d-8943-4852-bd4a-bdb463baf7b3)

El microservicio utiliza Python y flask para ejecutar el servidor, y Pytest para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` el cual contiene la logica de la aplicación y 1 carpeta test `test` para ejecutar las pruebas unitarias, así como algunos archivos de soporte.

### Archivos de soporte

- `Pipfile`: archivo de configuración de nuestra aplicacion de Python el cual contiene las dependiencias necesarias para su correcto funcionamiento, por ejemplo flask, SQlalquemy, pytest, etc.
- `Pipfile.lock`: archivo de detalle de las dependencias, el cual se crea automaticamente cuando ejecuto el comando Pipenv install
- `Dockerfile`: archivo de configuración de Docker para crear una imagen a partir de nuestra aplicación
- `.env.template`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente "productivo".
- `.env.test`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente de pruebas.

### Carpeta main

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/4b3ca88b-a3e2-4bbc-b7b8-ac5e4e9d02b4)

- En la raiz de la carpeta '/src' tenemos el archivo main.py el cual contiene la la configuración inicial de la aplicación y al declaración de sus servicios controladores

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/061e4435-9aef-4fdc-b017-52098e717ac3)

- En la carpeta '/configuración' tenemos una clase llamada de la misma manera, la cual setea en la variable app de flask las respectivas configuración e inicializa la configuración de la base de datos junto con su conexión

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/66bf12a6-6056-4e86-a7a5-7ae14b1e6e70)

- En la carpeta '/blueprints' existe un archivo llamado blueprints.py el cual contiene cada uno de los servicios a exponer

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/109e5e6e-d485-4590-afb7-b8039457d3c4)

- En la carpeta '/validators' existe un archivo llamado vlaidators.py el cual contiene las validaciones de cada servicio, con validaciones me refiero a validar el token, validar lso campos obligatorios, formatos de fechas, etc.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/489e5376-e257-4160-832e-63a3af586ebd)

- En la carpeta '/commands' existe un archivo llamado traecto_command.py el cual contiene la logica de negocio y transaccionabilidad, como crear ruta, consultar rutas existentes, eliminar, etc.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/c6219678-9848-463a-a3b7-306f7d8f202a)

- En la carpeta '/erros' tenemos un archivo llamado un archivo llamado errors.py el cual contiene todas las excepciones personalizadas las cuales estan creadas para devolver el codigo y mensaje solciitado en el enunciado

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/cd5ca037-faec-4dd8-a357-5e05451199e8)

- En la carpeta '/models' tenemos un archivo llamado models.py el cual contiene la entidad trayectos y schema asociado para la respectiva trasnformación a json

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/b8d93021-3a27-4202-b013-128d3dc07e19)

### Carpeta test

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/6b33afaa-c564-45c4-8f45-ad650c338d3d)

- En la ruta test tenemos un archivo en la raiz llamado conftest.py, este archivo nos permite configurar que los test tomen las variables de entorno de el archivo .env.test, para que la base de datos levante con la base de datos de memoria

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/cf040a37-69bc-405b-a9f0-cba24e387bd5)

- En el folder '/blueprint' tenemos un archivo llamado 'test_blueprint.py' el cual contiene las pruebas del archivo blueprint.py

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/e1889224-ac2f-4771-908e-e49981fd6dd8)

- En el folder '/command' tenemos el archivo 'test_command.py' el cual contiene las pruebas del los command declarados

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/0da23cf5-6d58-4408-b823-535446eaf612)

- En el folder '/validators' tenemos el archivo 'test_validators.py' el cual contiene las pruebas de los validators declarados

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/d2fc5c08-a810-408c-92ec-cb18281f3a42)

<a name="ejecutar-rutas"></a>

## 3. Ejecutar microservicio

### Instalar dependencias

- Activamos el entorno virtual, desde nuestro folder '/route' ejecutando el comando .\venv\Scripts\Activate, cuando se active, podremos ver desde la consola (venv)

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/2e36f561-6190-4c89-87d6-f30e42851e31)

- En la carpeta raiz ejecutamos el comando 'pipenv install'

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/8c986ad3-b0c1-4559-942f-6209aee47ffb)

### Variables de entorno

Nuestra aplicación utiliza variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución, esas variables son:

- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres

### Ejecutar aplicacion

Para ejecutar la aplicación nos situamos en la carpeta del microservicio /route, ejecutamos el comando $env:FLASK_APP = "src/main.py", este nos permite declarar que nuestro archivo principal es main.py

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/b24c9c69-d795-4d3d-915d-7e485f38bedb)

Ejeuctamos el comando 'flask run -h 0.0.0.0 -p 3002', este comando me permite levantar la aplicación en el puerto 3002

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/eb37467d-9cc9-45a3-a057-70cf04c8f30f)

### Ejecutar pruebas

Para ejecutar las pruebas unitarias del microservicios ejecuta el comando 'python -m pytest tests' desde la carpeta raíz del microservicio routes, en la consola podremos ver si las pruebas fueron exitosas:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/21a08a03-b3a0-4183-8035-40aefa70e69a)

Tambien podemos ejecutar el comando 'pipenv run pytest tests --cov=src -v -s --cov-fail-under=70' si queremos evidenciar el porcentaje de cobertura, especificando que este debe ser mayor de 70%

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/f622b30d-faba-4f86-81de-59f61e466ccc)

<a name="cobertura-pipeline-rutas"></a>

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática cuando se realiza push a la rama main y generará un error cuando la cobertura
de código - coverage no supere el 70%.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/7db76da5-b5f5-4d8b-ae98-12cb73335a0b)

resultado

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/172f1d49-5617-40ad-9760-2472dafd7a48)

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/b53f6219-f358-4f0b-b789-6a744044c9fd)

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

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

<a name="autor-rutas"></a>

## 6. Autor

Kevin Alexander Maldonado Delgado -`k.maldonadod@uniandes.edu.co`
