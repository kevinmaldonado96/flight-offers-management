import requests
import json
import base64
from google.cloud import pubsub_v1
import os

PROJECT_ID = 'entrega-2-nativas'
TOPIC_NAME_EMAIL='envio_correo_electronico'
TOPIC_NAME_ACTUALIZAR='actualizar_estado_tarjeta'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

def validar_estado_tarjeta(data_service_json, context):

    print(context)
    print(f'data_service_json {data_service_json}')

    mensaje = base64.b64decode(data_service_json["data"]).decode('utf-8')
    print(f"mensaje {mensaje}")

    data_service = json.loads(mensaje)

    path = data_service['trueNativePath']
    ruv = data_service['RUV']
    token = data_service['token']
    email = data_service['email']
    card_number =  data_service['cardNumber']
    issuer = data_service['issuer']

    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(f"{path}/native/cards/{ruv}", headers=headers, timeout=15)
    print(response)

    if response.status_code == 200:
        print(f'proceso exitosos {response}')

        data = response.json()

        mensaje = obtener_mensaje_email(email, card_number, issuer, data)
        encolar_mensaje(PROJECT_ID, TOPIC_NAME_EMAIL, mensaje)

        mensaje_actualizar = obtener_response_actualizar(data)
        actualizar_tarjeta_credito(path, mensaje_actualizar)

    else:
        raise Exception(f"Error en la petición codigo status : {response.status_code}")


def actualizar_tarjeta_credito(path, data):
    try:
        print(f"{path}/credit-cards/update")
        response = requests.put(f"{path}/credit-cards/update", json=data, timeout=15)
        print(f"response {response}")
    except Exception as e:
        print(f"Error a la hoa de actualizar la tarjeta de credito {e}")

def obtener_response_actualizar(data):
    datos = {
        "RUV": data['RUV'],
        "status": data['status']
    }
    return datos

def obtener_mensaje_email(email, card_number, issuer, data):

    datos = {
        "email": email,
        "subject": f"Estado validacion tarjeta {issuer} numero {card_number}",
        "content": f"<p>Su tarjeta {issuer} ha sido {data['status']}, para mas informaciOn comunicate con tu entidad bancaria mas cercana</p>"
    }

    json_string = json.dumps(datos)
    print(json_string)

    return json_string
    
def encolar_mensaje(project_id, topic_name, mensaje):
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project_id, topic_name)

    mensaje_bytes = mensaje.encode("utf-8")

    future = publisher.publish(topic_path, mensaje_bytes)
    print(f"Mensaje publicado en el topic {topic_path}: {mensaje}")
    future.result()  
    print(f"Mensaje publicado")

#datos = '{"trueNativePath": "http://34.111.30.70", "RUV": "cXdlcnR5MTIzNDU2OmVhZTI0Yjk1MzkxYWE4NDJiZjBhMjE4NTNhMjM1OGIyMmIxZDdlN2UwMjNmZjQ4OTI1NmM0YTYyYzc1NmJmNTg=", "token": "qwerty", "email": "k.maldonadod@uniandes.edu.co", "cardNumber": "12345", "issuer": "VISA"}'
#validar_estado_tarjeta(datos, '')