# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo():
    def __init__(self, repo):
        self.repo = repo
    
    def save_trip(self, trip):
        pass

    @staticmethod
    def license_allows(driver_license, vehicle_license):
        pass

    def finish_trip(self, trip_id):
        pass

    def save_only_trip(self, new_item):
        pass

    def save_trip_on_vehicle(self, plate):
        pass

    def save_trip_on_driver(self, driver_cpf):
        pass
    
    def save_trip_index_in_settings(self) -> None:
        pass
