# Projects imports
from vfms.repos.repo import Repo
from vfms.models.users.driver import Driver

class DriverRepo():
    def __init__(
        self : DriverRepo, 
        repo : Repo
    ):
        self.repo = repo

    def save_driver(
        self    : DriverRepo, 
        driver  : Driver,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM drivers WHERE cpf = ?", (driver.cpf,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo._cursor.execute("INSERT INTO drivers (name, cpf, license, xp, status) VALUES (?, ?, ?, ?, ?)", (driver.name, driver.cpf, driver.license.name, driver.xp, driver.status.name))
            self.repo._con.commit()

            return "Driver saved successfuly"

        return f"Already exists a driver with the {driver.cpf} cpf"

    def read_drivers(self) -> list:
        self.repo._cursor.execute("SELECT * FROM drivers")
        list_of_drivers = self.repo._cursor.fetchall()

        return list_of_drivers

    def read_driver_by_cpf(self, search_cpf) -> list:
        self.repo._cursor.execute("SELECT * FROM drivers WHERE cpf = ?", (search_cpf,))
        list_of_drivers = self.repo._cursor.fetchall()

        return list_of_drivers

    def delete_driver(self, search_cpf) -> str:
        self.repo._cursor.execute("SELECT * FROM drivers WHERE cpf = ?", (search_cpf,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This cpf doesn't exists on the table"

        self.repo._cursor.execute("DELETE FROM drivers WHERE cpf = ?", (search_cpf,))
        self.repo._con.commit()

        return f"The driver with cpf {search_cpf} was deleted."

    def driver_exists(self, search_cpf) -> bool:
        self.repo._cursor.execute("SELECT * FROM drivers WHERE cpf = ?", (search_cpf,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return False

        return True

    def driver_is_available(self, search_cpf) -> bool:
        self.repo._cursor.execute("SELECT * FROM drivers WHERE cpf = ? AND status = AVAILABLE", (search_cpf))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return False

        return True
