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
            origin      = request["origin"],
            destiny     = request["destiny"],
            distance    = request["distance"],
        )

        self.repo.save_trip(trip, request["driver_cpf"], request["vehicle_plate"])
