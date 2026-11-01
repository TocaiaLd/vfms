# standard libs
import json

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
    ):
        self.repo._cursor.execute("INSERT INTO trips (driver_cpf, vehicle_plate, origin, destiny, distance) VALUES (?, ?, ?, ?, ?)", (trip.driver_cpf, trip.vehicle_plate, trip.origin, trip.destiny, trip.distance))
        self.repo._con.commit()

        return "trip saved."

    def finish_trip(self, trip_id):
        pass