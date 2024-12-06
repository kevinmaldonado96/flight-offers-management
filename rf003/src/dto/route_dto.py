class RouteDTO:
   
   def __init__(self, flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate):
        self.flightId = flightId
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.plannedStartDate = plannedStartDate
        self.plannedEndDate = plannedEndDate

   def to_json(self):
        return {
            "flightId": self.flightId,
            "sourceAirportCode": self.sourceAirportCode,
            "sourceCountry": self.sourceCountry,
            "destinyAirportCode": self.destinyAirportCode,
            "destinyCountry": self.destinyCountry,
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate,
            "plannedEndDate": self.plannedEndDate
        }