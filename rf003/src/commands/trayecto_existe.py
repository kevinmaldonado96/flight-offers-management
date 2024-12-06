from .base_command import BaseCommannd
from ..rest.rest_client import GenericRestClient
from ..errors.errors import Rf003Exception
import os
import logging

class TrayectoExiste(BaseCommannd):

  def __init__(self, flight_id, headers):
    self.flight_id = flight_id
    self.headers = headers
  
  def ejecutar(self):

    logging.debug("Verificar trayecto existe")

    host_route = os.getenv('BASE_URL_ROUTE')

    params = {"flight": self.flight_id}
    url = f"{host_route}/routes"

    logging.debug(f"url {url}")

    genericRestClient = GenericRestClient(self.headers)
    response = genericRestClient.get(url, params=params)

    logging.debug(f"response {response}")
    content = response.json()

    logging.debug(f"content {content}")
    if response.status_code == 200:

      if len(content) > 0:
        return content[0]["id"]
      else:
        return None
    else:
      raise Rf003Exception(response.status_code, content["msg"]) 
