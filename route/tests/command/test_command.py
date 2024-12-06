from src.commands.trayecto_command import TrayectoCommand
from datetime import datetime, timedelta
from faker import Faker
fake = Faker()

trayecto_command = TrayectoCommand()

class TestCommand():

    def test_crear_trayecto(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        assert trayecto.id is not None

    def test_consultar_por_flight_id(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        trayecto_flight = trayecto_command.ver_trayetos_por_flightId(trayecto.flightId)
        assert trayecto_flight[0].get("flightId") == trayecto.flightId

    def test_consultar_por_flight_id_sin_parametro(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        trayecto_flight = trayecto_command.ver_trayetos_por_flightId(trayecto.flightId)
        assert len(trayecto_flight) > 0

    def test_consultar_por_flight_id_sin_parametro(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        trayecto_flight = trayecto_command.ver_trayetos_por_flightId(trayecto.flightId)
        assert len(trayecto_flight) > 0

    def test_consultar_trayecto_por_id(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        trayecto_id = trayecto_command.ver_trayetos_por_id(trayecto.id)
        assert trayecto_id.get("id") == trayecto.id

    def test_eliminar_trayecto_por_id(self):
        data = self.request_trayecto_exitoso_data()
        trayecto = trayecto_command.crear_trayecto(data)
        trayecto_command.eliminar_trayeto_por_id(trayecto.id)
        trayecto_id = trayecto_command.ver_trayetos_por_id(trayecto.id)
        assert not bool(trayecto_id)

    def request_trayecto_exitoso_data(self):
            start_date= self.generar_fecha()
            start_date_iso = self.generar_fecha_formato_iso8601(start_date)
            end_date = start_date + timedelta(days=5)
            end_date_iso = self.generar_fecha_formato_iso8601(end_date)
            data = {
                'flightId': fake.name(),
                'sourceAirportCode': fake.name(),
                'sourceCountry': fake.name(),
                'destinyAirportCode': fake.name(),
                'destinyCountry': fake.name(),
                'bagCost': fake.random_int(min=1, max=100),
                'plannedStartDate': start_date_iso,
                'plannedEndDate': end_date_iso}
            return data
    
    def generar_fecha(self):
        today = datetime.now()
        random_datetime = fake.date_time_between_dates(datetime_start=today+timedelta(days=1), datetime_end=today + timedelta(days=365))
        return random_datetime
    
    def generar_fecha_formato_iso8601(self, fecha_random):
        iso8601_with_milliseconds = fecha_random.isoformat(timespec='milliseconds') + 'Z'
        return iso8601_with_milliseconds