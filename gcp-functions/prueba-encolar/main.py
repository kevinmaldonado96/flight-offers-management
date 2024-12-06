from google.cloud import pubsub_v1
import os

def encolar_mensaje(project_id, topic_name, mensaje):
    # Crea un publicador
    publisher = pubsub_v1.PublisherClient()

    # Define la ruta del topic
    topic_path = publisher.topic_path(project_id, topic_name)

    # Codifica el mensaje en base64
    mensaje_bytes = mensaje.encode("utf-8")

    # Publica el mensaje
    future = publisher.publish(topic_path, mensaje_bytes)
    print(f"Mensaje publicado en el topic {topic_path}: {mensaje}")
    future.result()  # Bloquea hasta que se complete la publicación
    print(f"Mensaje publicado")


# Ejemplo de uso
if __name__ == "__main__":

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

    project_id = "uandes-native-416815"
    topic_name = "topic_estado_cuenta"
    mensaje = '{"trueNativePath": "http://34.111.30.70", "RUV": "MmZjOTU2NzctZjZiOC00ZGQzLWFkNzktZTA3Mzg1NTQzNjNhOmU1YTZiMjE3NDJjNGJkNGM5MDRmODFmOTgzMzYwNGM3MzViZTM2Yzk2MjIzNTI2YTAwNDlkODc2YzA1NTQxZTM=", "token": "qwerty", "email": "k.maldonadod@uniandes.edu.co", "cardNumber": "12345", "issuer": "VISA"}'

    encolar_mensaje(project_id, topic_name, mensaje)
