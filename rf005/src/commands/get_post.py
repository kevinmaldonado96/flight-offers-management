from os import environ
from .base_command import BaseCommannd
from src.errors.errors import PostNoExiste, CamposFaltantes, TrayectoNoExiste, OfertaNoExiste, PostNoAutorizado
from dotenv import load_dotenv
from src.utils.utils import FileUtils
import requests
import logging
import random

load_dotenv('.env.template')

POSTS_PATH = environ.get('POSTS_PATH')
ROUTES_PATH = environ.get('ROUTES_PATH')
OFFERS_PATH = environ.get('OFFERS_PATH')
SCORE_PATH = environ.get('SCORE_PATH')

class GetPost(BaseCommannd):
    def __init__(self, postId, headers, token):
        self.postId = postId
        self.headers = headers
        self.token = token

    def execute(self):
        post_data = self.get_post(self.postId)
        route_data = self.get_route(post_data['routeId'])
        offer_data = self.get_offer(self.postId)
        logging.debug(f"ID DEL POST {post_data['userId']}")
        user_id = FileUtils().get_user(self.headers)
        logging.debug(F"USUARIO DEL MS USER {user_id}")

        headers = {
            'Authorization': self.token
        }
        
        if post_data['userId'] != user_id:
            raise PostNoAutorizado

        if offer_data is not None:
            offers = []
            for offer in  offer_data:
                score_data = {
                    "offer": offer['offer'],
                    "size": offer['size'],
                    "bagCost": route_data['bagCost']
                }

                response = requests.post(url=SCORE_PATH + '/scores/calculate', json=score_data, headers=headers)
                score = response.json()

                logging.debug(f"CALCULATE {score}")

                offer_single = {
                    "id": offer['id'],
                    "userId": offer['userId'],
                    "description": offer['description'],
                    "size": offer['size'],
                    "fragile": offer['fragile'],
                    "offer": offer['offer'],
                    "score": score['value'],
                    "createdAt": offer['createdAt']
                }
                offers.append(offer_single)
            offers_sorted = sorted(offers, key=lambda d: d['score'], reverse=True) 
        else:
            raise OfertaNoExiste

        response_data = {
            "id": post_data['id'],
            "expireAt": post_data['expireAt'],
            "route": {
                "id": route_data['id'],
                "flightId": route_data['flightId'],
                "origin": {
                    "airportCode": route_data['sourceAirportCode'],
                    "country": route_data['sourceCountry']
                },
                "destiny": {
                    "airportCode": route_data['destinyAirportCode'],
                    "country": route_data['destinyCountry']
                },
                "bagCost": route_data['bagCost']
            },
            "plannedStartDate": route_data['plannedStartDate'],
            "plannedEndDate": route_data['plannedEndDate'],
            "createdAt": post_data['createdAt'],
            "offers": offers_sorted
        }

        return response_data
    
    def get_post(self, postId):
        if not postId:
            raise CamposFaltantes

        headers = {
            'Authorization': self.token
        }

        response = requests.get(url=POSTS_PATH + '/posts/'+postId, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if (len(data) >= 1):
                return data
            else:
                logging.debug('Post no encontrado')
                return None
        else:
            raise PostNoExiste
    
    def get_route(self, routeId):
        if not routeId:
            raise CamposFaltantes

        headers = {
            'Authorization': self.token
        }

        response = requests.get(url=ROUTES_PATH + '/routes/'+routeId, headers=headers)
       
        if response.status_code == 200:
            data = response.json()
            
            if (len(data) >= 1):
                return data
            else:
                logging.debug('Trayecto no encontrado')
                return None
        else:
            raise TrayectoNoExiste
    
    def get_offer(self, postId):
        if not postId:
            raise CamposFaltantes

        headers = {
            'Authorization': self.token
        }
        
        response = requests.get(url=OFFERS_PATH + '/offers?post='+postId, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
        
            if (len(data) >= 1):
                return data
            else:
                logging.debug('Oferta no encontrada')
                return None
        else:
            raise OfertaNoExiste
        