# Projects imports
from vfms.repos.refuel_repo import RefuelRepo

class RefuelController:
    def __init__(
        self : RefuelController,
        repo : RefuelRepo
    ):
        self.repo = repo
    
    def save_refuel(
        self            : RefuelController, 
        maintenance     : tuple
    ):
        return self.repo.save_refuel(maintenance)