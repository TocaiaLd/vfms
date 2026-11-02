from typing import Any

# External libs
from tabulate import tabulate

# Projects imports
from vfms.repos.trip_repo import TripRepo
from vfms.models.trip import Trip

class TripController:
    # Coordinate trip creation, lookup, completion, and display.
    def __init__(
        self    : TripController,
        repo    : TripRepo,
    ) -> None:
        self.repo   = repo

    def new_trip(self, request: dict[str, Any]) -> str:
        trip = Trip(
            driver_cpf      = request["driver_cpf"],
            vehicle_plate   = request["vehicle_plate"],
            origin          = request["origin"],
            destiny         = request["destiny"],
            distance        = request["distance"],
            status          = request["status"]
        )

        trip.set_date_init()

        return self.repo.save_trip(trip)

    def get_trip_by_id(self, trip_id: str) -> Trip | bool:
        trip = self.repo.get_trip_by_id(trip_id)
        
        if trip:
            trip = Trip(
                driver_cpf    = trip[0][1],
                vehicle_plate = trip[0][2],  
                origin        = trip[0][3],  
                destiny       = trip[0][4],
                distance      = trip[0][5],
                status        = trip[0][6]
            )

            return trip
        
        return False

    def finish_trip(self, trip_id: str) -> str:
        trip: Trip | bool = self.get_trip_by_id(trip_id)
        
        if trip:
            if trip.status.name == "ENDED":
                return "This trips was already ended"
            
            trip.set_date_end()
            return self.repo.finish_trip(trip, trip_id)

        return "this trip doenst exists"

    def show_trips(self) -> str:
        response = self.repo.read_trips()

        collumns = ["trip_id", "driver_cpf", "vehicle_plate", "origin", "destiny", "distance", "status", "date_init", "date_end"]
        data = []

        for d in response:
            data.append([d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8]])
    
        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response
