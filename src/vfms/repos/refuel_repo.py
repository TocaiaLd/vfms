from typing import Any

# Projects imports
from vfms.repos.repo import Repo

class RefuelRepo():
    def __init__(
        self : RefuelRepo, 
        repo : Repo
    ) -> None:
        self.repo = repo

    def save_refuel(
        self            : RefuelRepo, 
        maintenance     : tuple[Any, ...]
    ) -> None:
        self.repo._cursor.execute("INSERT INTO refuels (plate, liters, price_per_liter, total_cost, date) VALUES (?, ?, ?, ?, ?)", maintenance)
        self.repo._con.commit()
