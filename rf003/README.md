# Microservicio RF003

## Tabla de contenido

1. [Pre-requisitos](#pre-requisito-rutas)
2. [Estructura microservicio](#estructura-rutas)
   - [Archivos de soporte](#archivos-de-soporte)
   - [Carpeta main](#Carpeta-src)
   - [Carpeta test](#Carpeta-test)
3. [Ejecutar microservicio](#Ejecutar-rutas)
   - [Instalar dependencias](#Instalar-dependencias)
   - [Variables de entorno](#variables-de-entorno)
   - [Ejecutar aplicacion](#jecutar-aplicacion)
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

Inicialmente la estructura de proyecto esta distribuida de la siguiente manera:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/6c865553-e825-4c66-b0fb-faa054f1e78c)

El microservicio utiliza Python y flask para ejecutar el servidor, y Pytest para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` el cual contiene la logica de la aplicación y 1 carpeta test `test` para ejecutar las pruebas unitarias, así como algunos archivos de soporte.

### Archivos de soporte

- `Pipfile`: archivo de configuración de nuestra aplicacion de Python el cual contiene las dependiencias necesarias para su correcto funcionamiento, por ejemplo flask, SQlalquemy, pytest, etc.
- `Pipfile.lock`: archivo de detalle de las dependencias, el cual se crea automaticamente cuando ejecuto el comando Pipenv install.
- `Dockerfile`: archivo de configuración de Docker para crear una imagen a partir de nuestra aplicación.
- `.env.template`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente "productivo".
- `.env.test`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente de pruebas.

### Carpeta src

- En la raiz de la carpeta '/src' tenemos el archivo main.py el cual contiene la la configuración inicial de la aplicación y al declaración de sus servicios controladores.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/b4c7394f-cda1-4c11-b30f-1507ff7897fc)

- En la carpeta '/blueprints' existe un archivo llamado blueprints.py el cual contiene cada uno de los servicios a exponer.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/5b497bf7-d719-44a3-bdcf-56ab1f83c6db)

- En la carpeta '/validators' existe un archivo llamado validator.py el cual contiene las validaciones para cada servicio, como validación de token y campos obligatorios.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/c08242d4-ea32-42b7-9b92-290bf668d5c1)

- En la carpeta '/commands' existen fiferentes archivos como crear_post.py, trayecto_existe.py, eliminar_trayecto.py, post_existe.py y crear_trayecto.py, cada uno representa una tarea dnetro del patron de cadena, cada uno tiene la logica de negocio necesaria para llamar a los microservicios de Trayectos y Posts.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/623f2265-4851-488b-9190-bfa244113256)

Ejemplo crear_posts.py

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/82a88a12-a74f-41ef-bedc-290b7d3b6687)

- En la carpeta '/errors' tenemos un archivo llamado un archivo llamado errors.py el cual contiene una excepción generica que permite personalizar los mensajes y codigos definidos en el acuerdo de interfaz.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/e8023601-b6ff-44f3-847c-611d25b72c33)

- En la carpeta /rest vemos unrchivo llamado rest_client.py a cliente rest generico el cual centralizar los llamados de los servicios rest

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/3b0ef87d-ee75-4bff-bd1d-92a0ca11f1b6)


### Carpeta test

- En la ruta test tenemos un archivo en la raiz llamado conftest.py, este archivo nos permite configurar que los test tomen las variables de entorno de el archivo .env.test, para que ome los endpoints de prueba.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/78cde6cb-68d2-4543-9b47-3973cb30b18d)

- En el folder '/blueprints' tenemos un archivo llamado 'test_blueprints.py' el cual contiene las pruebas unitarias de los blueprints.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/103daf43-043a-43bc-8f66-c39b48e83507)

- En el folder '/commands' tenemos un archivo llamado 'test_blueprints.py' el cual contiene las pruebas unitarias de los commands

  ![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/46cf243d-db0a-477f-b433-0c28833f0b46)

- En el folder '/validators' tenemos un archivo llamado 'test_blueprints.py' el cual contiene las pruebas unitarias de los commands

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/502d87eb-e193-419a-bcf3-c3767ccc9562)

<a name="ejecutar-rutas"></a>

## 3. Ejecutar microservicio

### Ejecutar aplicacion

Ejecucion solo mediante flash

```
FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3006
```

Para construir la imagen, situarse en la carpeta rf003

```
docker build -t rf003 .
```

Ejecucion para iniciar el contenedor para rf003

Para ejecutar el microservicio, se debe ejecutar el comando docker-compose up --build para levantar cada uno de los contenedores, el archivo docker compose se encuentra en la carpeta raiz, por ende se debe ejecutar dicha publicacion
```
docker compose up --build
```

Para ejeuctar el microservicio a traves de kubernates, debe situarse en la carpeta llamada kubernetes, alli se encuentran los archivos de configuración 

k8s-base-layers-deployment.yaml: archivo con microservicios entrega 1
k8s-ingress-deployment.yaml: archivo con el ingress para comunicarnos con los microservicios
k8s-new-services-depoyment: archivo con los nuevos microservicios, sus services y backconfig 
k8s-secrets.yaml: archivo con secretos

Debes ejecutar el comando
```
k8s apply -f [NOMBRE DLE ARHCIVO K8S]
```

### Ejecutar pruebas

Puede correr el grupo de pruebas unitarias y generar el reporte mediante el siguiente comando:

```
pytest --cov-fail-under=70 --cov=src --cov-report=html
```

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática cuando se realiza push a la rama main y generará un error cuando la cobertura
de código - coverage no supere el 70%.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/27ec0b40-801d-495f-b655-70639acf174f)

Resultado:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123959005/8df963be-c07a-4800-aa60-635a6dbff6d8)

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

Kevin Alexander Maldonado Delgado - k.maldonadod@uniandes.edu.co
