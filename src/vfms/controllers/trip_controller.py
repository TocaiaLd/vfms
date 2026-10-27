# Projects imports
from vfms.repos.trip_repo import TripRepo
from vfms.models.trip import Trip

class TripController:
    def __init__(
        self    : TripController,
        repo    : TripRepo,
    ):
        self.repo   = repo

    def new_trip(self, request):
        trip = Trip(
            driver_cpf      = request["driver_cpf"],
            vehicle_plate   = request["vehicle_plate"],
            origin          = request["origin"],
            destiny         = request["destiny"],
            distance        = request["distance"],
        )

        self.repo.save_trip(trip)

    def finish_trip(self, trip_id):
        return self.repo.finish_trip(str(trip_id))
