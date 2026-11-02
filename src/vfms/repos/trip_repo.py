# standard libs
from vfms.enums.enum_trip import EnumTrip
from vfms.enums.driver_status import DriverStatus
from vfms.enums.vehicle_status import VehicleStatus


# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo():
    def __init__(
        self    : TripRepo, 
        repo    : Repo
    ):
        self.repo = repo
    
    def save_trip(
        self : TripRepo, 
        trip : Trip
    ) -> str:

        types = ["cars", "trucks", "motorcycles"]

        for n in types:
            self.repo._cursor.execute(f"SELECT * FROM {n} WHERE PLATE = ?", (trip.vehicle_plate,))
            result = self.repo._cursor.fetchall()

            if result:
                self.repo._cursor.execute(f"UPDATE {n} SET status = ? WHERE plate = ?;", (VehicleStatus.ON_TRIP.name, trip.vehicle_plate))
                self.repo._con.commit()
                break
            
        self.repo._cursor.execute(f"UPDATE drivers SET status = ? WHERE cpf = ?;", (DriverStatus.ON_TRIP.name, trip.driver_cpf))
        self.repo._con.commit()

        self.repo._cursor.execute("INSERT INTO trips (driver_cpf, vehicle_plate, origin, destiny, distance, status, date_init, date_end) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (trip.driver_cpf, trip.vehicle_plate, trip.origin, trip.destiny, trip.distance, trip.status.value, trip.date_init, "..."))
        self.repo._con.commit()

        return "trip saved."

    def finish_trip(
        self    : TripRepo, 
        trip    : Trip,
        trip_id : str,   
    ):
        int_trip_id = int(trip_id)
        
        from vfms.depedencies import settings
        preventive_interval = settings["maintenance"]["preventive_interval_km"]

        types = ["cars", "trucks", "motorcycles"]

        for n in types:
            self.repo._cursor.execute(f"SELECT * FROM {n} WHERE PLATE = ?", (trip.vehicle_plate,))
            result = self.repo._cursor.fetchall()

            if result:
                self.repo._cursor.execute(f"UPDATE {n} SET status = ?, mileage = mileage + ? WHERE plate = ?;", (VehicleStatus.AVAILABLE.name, trip.distance, trip.vehicle_plate))
                self.repo._con.commit()
                
                # Get the previous and current mileage
                mileage_old = result[0][4]
                mileage_current = mileage_old + trip.distance

                # Check if the vehicle crossed a preventive maintenance interval
                if mileage_current // preventive_interval > mileage_old // preventive_interval:

                    self.repo._cursor.execute(
                        f"UPDATE {n} SET status = ? WHERE plate = ?;",
                        (VehicleStatus.MAINTENANCE.name, trip.vehicle_plate)
                    )

                    self.repo._con.commit()

                break
            
        self.repo._cursor.execute("UPDATE drivers SET status = ? WHERE cpf = ?;", (DriverStatus.AVAILABLE.name, trip.driver_cpf))
        self.repo._con.commit()

        self.repo._cursor.execute("UPDATE trips SET status = ?, date_end = ? WHERE trip_id = ?;", (EnumTrip.ENDED.value, trip.date_end, int_trip_id))
        self.repo._con.commit()

        return "trip finished."

    def get_trip_by_id(self, trip_id) -> tuple | False:
        self.repo._cursor.execute("SELECT * FROM trips WHERE trip_id = ?", (trip_id,))
        trip = self.repo._cursor.fetchall()

        if trip:
            return trip
        
        return False

    def read_trips(self) -> list:
        self.repo._cursor.execute("SELECT * FROM trips")
        trips = self.repo._cursor.fetchall()

        return trips