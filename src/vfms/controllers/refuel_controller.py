# Projects imports
from vfms.repos.refuel_repo import RefuelRepo

class RefuelController:
    # Coordinate persistence of refueling records.
    def __init__(
        self : RefuelController,
        repo : RefuelRepo
    ) -> None:
        self.repo = repo
    
    def save_refuel(
        self    : RefuelController, 
        refuel  : tuple[object, ...]
    ) -> None:
        return self.repo.save_refuel(refuel)
