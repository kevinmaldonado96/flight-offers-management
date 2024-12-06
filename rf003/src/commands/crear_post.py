from .base_command import BaseCommannd
from ..rest.rest_client import GenericRestClient
from ..commands.eliminar_trayecto import EliminarTrayecto
from ..errors.errors import Rf003Exception
from ..dto.post_dto import PostDTO
import os

class CrearPost(BaseCommannd):

  def __init__(self, route_id, es_route_nuevo, expire_at, headers):
    self.route_id = route_id
    self.expire_at = expire_at
    self.headers = headers
    self.es_route_nuevo = es_route_nuevo
  
  def ejecutar(self):

    host_route = os.getenv('BASE_URL_POST')

    url = f"{host_route}/posts"

    genericRestClient = GenericRestClient(self.headers)

    request_dto = self.obtener_request_post()
    response = genericRestClient.post(url, data=request_dto.to_json())

    content = response.json()

    if response.status_code == 201:
      return content
    else:
      if self.es_route_nuevo:
        eliminar_trayecto = EliminarTrayecto(self.route_id, self.headers)
        eliminar_trayecto.ejecutar()

      raise Rf003Exception(response.status_code, content["msg"]) 
    
  def obtener_request_post(self):
      
        routeId = self.route_id
        expireAt = self.expire_at
        
        return PostDTO(routeId, expireAt)