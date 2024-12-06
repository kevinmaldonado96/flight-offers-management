# Microservicio RF005

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

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/9da2b568-ce36-4020-beab-100623132d71)

El microservicio utiliza Python y flask para ejecutar el servidor, y Pytest para ejecutar las pruebas unitarias. Dentro de este hay 1 carpeta principal `src` el cual contiene la logica de la aplicación y 1 carpeta test `test` para ejecutar las pruebas unitarias, así como algunos archivos de soporte.

### Archivos de soporte

- `Pipfile`: archivo de configuración de nuestra aplicacion de Python el cual contiene las dependiencias necesarias para su correcto funcionamiento, por ejemplo flask, SQlalquemy, pytest, etc.
- `Pipfile.lock`: archivo de detalle de las dependencias, el cual se crea automaticamente cuando ejecuto el comando Pipenv install.
- `Dockerfile`: archivo de configuración de Docker para crear una imagen a partir de nuestra aplicación.
- `.env.template`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente "productivo".
- `.env.test`: archivo de variables de entorno de nuestra aplicación, el cual contiene por ejemplo las variables de entorno de base de datos, etc, este archivo se usa cuando la aplicación correo en un ambiente de pruebas.

### Carpeta src

- En la raiz de la carpeta '/src' tenemos el archivo main.py el cual contiene la la configuración inicial de la aplicación y al declaración de sus servicios controladores.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/70deb308-1cb9-4022-a27d-9b33fae0c07a)

- En la carpeta '/blueprints' existe un archivo llamado operations.py el cual contiene cada uno de los servicios a exponer.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/d6d41e6c-cb4d-414b-9d6c-5f9e27bd1e8d)

- En la carpeta '/validators' existe un archivo llamado validator.py el cual contiene las validaciones para cada servicio, como validación de token.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/d047ac09-f7a2-4949-bb6b-7e6005a75b94)

- En la carpeta '/commands' existe el archivo get_post.py, el cual contiene la logica de negocio y transaccionabilidad, como consultar publicaciones, rutas, ofertas, etc.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/08c35661-c61a-4593-a9dc-8efeac147abf)

- En la carpeta '/errors' tenemos un archivo llamado un archivo llamado errors.py el cual contiene todas las excepciones personalizadas las cuales estan creadas para devolver el codigo y mensaje solcitado en el enunciado.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/c9ff4aa3-e289-49c6-8789-a6c4a3e28e39)

### Carpeta test

- En la ruta test tenemos un archivo en la raiz llamado conftest.py, este archivo nos permite configurar que los test tomen las variables de entorno de el archivo .env.test, para que la base de datos levante con la base de datos de memoria

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/5213e11b-b19e-4cf7-a3b7-2f0728f24f32)

- En el folder '/blueprints' tenemos un archivo llamado 'test_rf005.py' el cual contiene las pruebas.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/da3011fd-e518-4876-81c1-577628d10975)

<a name="ejecutar-rutas"></a>

## 3. Ejecutar microservicio

### Ejecutar aplicacion

Ejecucion solo mediante flash
```
FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3005
```

Para construir la imagen, situarse en la carpeta rf005
```
docker build -t rf005 .
```

Ejecucion para iniciar el contenedor para rf005
```
docker run --env-file ./.env.template -p 3005:3005 rf005
```

### Ejecutar pruebas

Puede correr el grupo de pruebas unitarias y generar el reporte mediante el siguiente comando:

```
pytest --cov-fail-under=70 --cov=src --cov-report=html
```

### Verificar cobertura en pipeline

La validación de cobertura se hace de forma automática cuando se realiza push a la rama main y generará un error cuando la cobertura
de código - coverage no supere el 70%.

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/ba7bd9af-8131-479a-b8e3-cf63c1d52c77)

Resultado:

![image](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo14/assets/123951967/ad33740d-753d-48d6-af2d-34c8226ef6c3)

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
Luisa Johanna Torres Moncaleano - lj.torresm1@uniandes.edu.co
