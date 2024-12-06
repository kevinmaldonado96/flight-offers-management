from .base_command import BaseCommannd
from ..rest.rest_client import GenericRestClient
from ..errors.errors import Rf003Exception
from ..dto.route_dto import RouteDTO
import os
import logging

class CrearTrayecto(BaseCommannd):

  def __init__(self, data, headers):
    self.data = data
    self.headers = headers
  
  def ejecutar(self):

    logging.debug("creación de trayecto")
    host_route = os.getenv('BASE_URL_ROUTE')

    url = f"{host_route}/routes"

    logging.debug(f"headers {self.headers}")
    genericRestClient = GenericRestClient(self.headers)

    request_dto = self.obtener_request_route()
    response = genericRestClient.post(url, data=request_dto.to_json())

    content = response.json()

    if response.status_code == 201:
      return content["id"]
    else:
      raise Rf003Exception(response.status_code, content["msg"]) 
    
  def obtener_request_route(self):
      
        flightId = self.data.get('flightId')

        origin = self.data.get('origin')
        sourceAirportCode = origin.get('airportCode')
        sourceCountry = origin.get('country')

        destiny = self.data.get('destiny')
        destinyAirportCode = destiny.get('airportCode')
        destinyCountry = destiny.get('country')

        bagCost = self.data.get('bagCost')
        plannedStartDate = self.data.get('plannedStartDate')
        plannedEndDate = self.data.get('plannedEndDate')

        return RouteDTO(flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate)