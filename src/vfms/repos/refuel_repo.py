from typing import Any
from datetime import datetime
import sqlite3

# Projects imports
from vfms.repos.repo import Repo
from vfms.exceptions import RepositorioError

class RefuelRepo():
    # Persist fuel purchase records.
    def __init__(
        self : RefuelRepo, 
        repo : Repo
    ) -> None:
        self.repo = repo

    def save_refuel(
        self            : RefuelRepo, 
        maintenance     : tuple[Any, ...]
    ) -> None:
        values = list(maintenance)
        if isinstance(values[4], datetime):
            values[4] = values[4].isoformat(timespec="seconds")
        try:
            with self.repo._con:
                self.repo.execute(
                    "INSERT INTO refuels (plate, liters, price_per_liter, total_cost, date) VALUES (?, ?, ?, ?, ?)",
                    tuple(values),
                )
        except sqlite3.Error as exc:
            raise RepositorioError("Could not save refuel record") from exc
