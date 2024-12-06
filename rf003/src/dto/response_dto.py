import datetime

class ResponseDTO:
   
   def __init__(self, id, userId, expireAt, id_route):
        fecha_actual = datetime.datetime.now()

        self.id = id
        self.userId = userId
        self.expireAt = expireAt
        self.id_route = id_route
        self.create_at = fecha_actual.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

   def to_json(self):
       return {
           "data": {
               "id": self.id,
               "userId": self.userId,
               "createdAt": self.create_at,
               "expireAt": self.expireAt,
               "route": {
                   "id": self.id_route,
                   "createdAt": self.create_at
               }
           },
           "msg": "transaccion realizada con exito"
       }