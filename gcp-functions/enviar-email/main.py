import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
import base64

TOKEN_SENDGRID = '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'
FROM_EMAIL='k_maldonado12@hotmail.com'

def send_email(data_service_64, context):

    print(context)
    print(f'data_service_json {data_service_64}')

    mensaje = base64.b64decode(data_service_64['data']).decode('utf-8')
    print(f"mensaje {mensaje}")

    data_service = json.loads(mensaje)

    email = data_service['email']
    subject = data_service['subject']
    content = data_service['content']

    print(f" email {email} subject {subject} content {content}")

    sg = SendGridAPIClient(TOKEN_SENDGRID)

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=f"<p>{content}</p>"
    )

    try:
        response = sg.send(message)
        print('Enviado con exito')
        return {"status_code": response.status_code}
    
    except Exception as e:
        print("error: ", e)


#datos = '{"email": "lj.torresm1@uniandes.edu.co", "subject": "prueba envio email sendgrid", "content": "funciona el envio perros"}'
#send_email(datos, '')



