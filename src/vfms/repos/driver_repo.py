from typing import Any
import sqlite3

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.users.driver import Driver
from vfms.exceptions import RepositorioError
from vfms.enums.driver_status import DriverStatus

class DriverRepo():
    # Read and write driver records through the shared SQLite repository.
    def __init__(
        self : DriverRepo, 
        repo : Repo
    ) -> None:
        self.repo = repo

    def save_driver(
        self    : DriverRepo, 
        driver  : Driver,
    ) -> str:
        self.repo.execute("SELECT * FROM drivers WHERE cpf = ?", (driver.cpf,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo.execute("INSERT INTO drivers (name, cpf, license, xp, status) VALUES (?, ?, ?, ?, ?)", (driver.name, driver.cpf, driver.license.name, driver.xp, driver.status.name))
            self.repo.commit()

            return "Driver saved successfuly"

        return f"Already exists a driver with the {driver.cpf} cpf"

    def read_drivers(self) -> list[tuple[Any, ...]]:
        self.repo.execute("SELECT * FROM drivers")
        list_of_drivers = self.repo._cursor.fetchall()

        return list_of_drivers

    def read_driver_by_cpf(self, search_cpf: str) -> list[tuple[Any, ...]]:
        self.repo.execute("SELECT * FROM drivers WHERE cpf = ?", (search_cpf,))
        list_of_drivers = self.repo._cursor.fetchall()

        return list_of_drivers

    def delete_driver(self, search_cpf: str) -> str:
        with self.repo._con:
            driver = self.repo.execute(
                "SELECT 1 FROM drivers WHERE cpf = ?", (search_cpf,)
            ).fetchone()
            if driver is None:
                return "This CPF does not exist in the table"

            trip = self.repo.execute(
                "SELECT 1 FROM trips WHERE driver_cpf = ? LIMIT 1", (search_cpf,)
            ).fetchone()
            if trip is not None:
                return "Cannot delete a driver with recorded trips"

            self.repo.execute(
                "DELETE FROM drivers WHERE cpf = ?", (search_cpf,)
            )

        return f"The driver with cpf {search_cpf} was deleted."

    def driver_exists(self, search_cpf: str) -> bool:
        self.repo.execute("SELECT * FROM drivers WHERE cpf = ?", (search_cpf,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return False

        return True

    def driver_is_available(self, search_cpf: str) -> bool:
        try:
            self.repo.execute(
                "SELECT 1 FROM drivers WHERE cpf = ? AND status = ?",
                (search_cpf, DriverStatus.AVAILABLE.name),
            )
            return self.repo._cursor.fetchone() is not None
        except sqlite3.Error as exc:
            raise RepositorioError("Could not check driver availability") from exc

    def get_by_cpf(self, cpf: str) -> tuple[Any, ...] | None:
        self.repo.execute(f"SELECT * from drivers WHERE cpf = ?", (cpf,))
        driver = self.repo._cursor.fetchone()

        return driver

    def update_driver(
        self    : DriverRepo,
        driver  : Driver
    ) -> str:
        exists = self.repo.execute(
            "SELECT 1 FROM drivers WHERE cpf = ?", (driver.cpf,)
        ).fetchone()
        if exists is None:
            return f"No driver exists with cpf {driver.cpf}"

        new_data = (driver.name, driver.license.name, driver.xp, driver.status.name, driver.cpf)
        
        self.repo.execute("""
UPDATE drivers 
SET name = ?, license = ?, xp = ?, status = ?  
WHERE cpf = ?;
""", new_data)
        self.repo.commit()
        return "Driver updated successfuly"



