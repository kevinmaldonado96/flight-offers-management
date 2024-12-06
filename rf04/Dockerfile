# Etapa de construcción
FROM gradle:jdk17 as builder

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código fuente de la aplicación Spring Boot al contenedor
COPY . .

# Compila la aplicación Spring Boot con Gradle
RUN ./gradlew build -x test

# Utiliza una imagen base más ligera de OpenJDK para la aplicación final
FROM openjdk:17-jdk

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo JAR compilado de la aplicación Spring Boot al contenedor
COPY --from=builder /app/build/libs/rf04.jar /app

# Puerto
EXPOSE 3004

# Comando para ejecutar la aplicación Spring Boot al iniciar el contenedor
CMD ["java", "-jar", "rf04.jar"]