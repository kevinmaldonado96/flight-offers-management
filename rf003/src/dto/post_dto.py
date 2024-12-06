class PostDTO:

    def __init__(self, routeId, expireAt):
        self.routeId = routeId
        self.expireAt = expireAt

    def to_json(self):
        return {
            "routeId": self.routeId,
            "expireAt": self.expireAt
        }