from .base_command import BaseCommannd
from ..rest.rest_client import GenericRestClient
from ..errors.errors import Rf003Exception
import os

class EliminarTrayecto(BaseCommannd):

  def __init__(self, route_id, headers):
    self.route_id = route_id
    self.headers = headers
  
  def ejecutar(self):

    host_route = os.getenv('BASE_URL_ROUTE')
    url = f"{host_route}/routes/{self.route_id}"

    genericRestClient = GenericRestClient(self.headers)
    response = genericRestClient.delete(url)

    content = response.json()

    if response.status_code == 200:
      return True
    else:
      raise Rf003Exception(response.status_code, content["msg"]) 