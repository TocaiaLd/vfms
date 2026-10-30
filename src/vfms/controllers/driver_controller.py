# External libs
from vfms.repos.driver_repo import DriverRepo
from tabulate import tabulate

# Projects imports
from vfms.models.users.driver import Driver

class DriverController:
    def __init__(
        self : DriverController, 
        repo : DriverRepo
    ):
        self.repo = repo
    
    def new_driver(self, request) -> str:
        driver = Driver(
            name            = request["name"],
            cpf             = request["cpf"],
            license         = request["license"],
            xp              = request["xp"],
            status          = request["status"],
        )

        return self.repo.save_driver(driver)

    def show_drivers(self) -> str:
        response = self.repo.read_drivers()

        collumns = ["Name", "CPF", "License", "Experience", "Status"]
        data = []

        for d in response:
            data.append([d[0], d[1], d[2], d[3], d[4]])
    
        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response
    
    def show_driver_by_cpf(self, search_cpf) -> str:
        response = self.repo.read_driver_by_cpf(search_cpf)

        collumns = ["Name", "CPF", "License", "Experience", "Status"]
        data = []

        for d in response:
            data.append([d[0], d[1], d[2], d[3], d[4]])
    
        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response

    def delete_driver(self, search_cpf) -> str:
        response = self.repo.delete_driver(search_cpf)
        return response