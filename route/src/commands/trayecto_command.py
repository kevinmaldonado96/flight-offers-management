from ..models.models import Trayecto, TrayectosSchema, db
from datetime import datetime
import logging

trayecto_schema = TrayectosSchema()

class TrayectoCommand():
    def crear_trayecto(self, datos_trayecto):
        self.flightId = datos_trayecto.get('flightId')
        self.sourceAirportCode = datos_trayecto.get('sourceAirportCode')
        self.sourceCountry = datos_trayecto.get('sourceCountry')
        self.destinyAirportCode = datos_trayecto.get('destinyAirportCode')
        self.destinyCountry = datos_trayecto.get('destinyCountry')
        self.bagCost = datos_trayecto.get('bagCost')
        self.plannedStartDate = datos_trayecto.get('plannedStartDate')
        self.plannedEndDate = datos_trayecto.get('plannedEndDate')

        fecha_start_parseada = self.obtener_fecha_parseada(self.plannedStartDate)
        fecha_end_parseada = self.obtener_fecha_parseada(self.plannedEndDate)


        trayecto = Trayecto(             
            flightId = self.flightId,
            sourceAirportCode = self.sourceAirportCode,
            sourceCountry = self.sourceCountry,
            destinyAirportCode =self.destinyAirportCode,
            destinyCountry = self.destinyAirportCode,
            bagCost = self.bagCost,
            plannedStartDate = fecha_start_parseada,
            plannedEndDate = fecha_end_parseada
        )

        db.session.add(trayecto)
        db.session.commit()

        return trayecto
      
    def ver_trayetos_por_flightId(self, flightId):
        if flightId is not None:
            trayectos = self.consultar_trayecto_por_flightId(flightId)
        else:
            trayectos = db.session.query(Trayecto).all()
            
        trayectos_schema = [trayecto_schema.dump(trayecto) for trayecto in trayectos]
        return trayectos_schema

    def ver_trayetos_por_id(self, id_trayecto):
        trayecto = self.consultar_trayecto_por_id(id_trayecto)
        return trayecto_schema.dump(trayecto)
    
    def eliminar_trayeto_por_id(self, id_trayecto):
        trayecto = self.consultar_trayecto_por_id(id_trayecto)
        db.session.delete(trayecto)
        db.session.commit()

    def consultar_trayecto_por_id(self, id_trayecto):
        return db.session.query(Trayecto).filter_by(id=id_trayecto).first() 
    
    def consultar_trayecto_por_flightId(self, flightId):
        return db.session.query(Trayecto).filter(Trayecto.flightId.like(f'%{flightId}')).all() 

    def reset(self):
        db.session.query(Trayecto).delete()
        db.session.commit()

    def obtener_fecha_parseada(self, fecha_request):
        fecha_parseada = datetime.strptime(fecha_request, '%Y-%m-%dT%H:%M:%S.%fZ')
        return fecha_parseada