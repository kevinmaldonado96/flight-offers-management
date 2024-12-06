from .base_command import BaseCommannd
from ..rest.rest_client import GenericRestClient
from ..errors.errors import Rf003Exception
import os
import logging

class PostExiste(BaseCommannd):

  def __init__(self, route_id, headers):
    self.route_id = route_id
    self.headers = headers
  
  def ejecutar(self):

    host_route = os.getenv('BASE_URL_POST')

    params = {"routeId": self.route_id, "owner": "me"}
    url = f"{host_route}/posts"

    genericRestClient = GenericRestClient(self.headers)
    response = genericRestClient.get(url, params=params)

    logging.debug(f"response {response}")
    content = response.json()

    logging.debug(f"content {content}")
    if response.status_code == 200:
      if len(content) > 0:
        raise Rf003Exception(412, "El usuario ya tiene una publicación para la misma fecha")
    else:
      raise Rf003Exception(response.status_code, content["msg"]) 
