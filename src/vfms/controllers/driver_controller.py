from typing import Any

# External libs
from tabulate import tabulate

# Projects imports
from vfms.enums.driver_status import DriverStatus
from vfms.enums.vehicle_license import VehicleLicense
from vfms.repos.driver_repo import DriverRepo
from vfms.models.users.driver import Driver

class DriverController:
    def __init__(
        self : DriverController, 
        repo : DriverRepo
    ) -> None:
        self.repo = repo
    
    def new_driver(self, request: dict[str, Any]) -> str:
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
    
    def show_driver_by_cpf(self, search_cpf: str) -> str:
        response = self.repo.read_driver_by_cpf(search_cpf)

        collumns = ["Name", "CPF", "License", "Experience", "Status"]
        data = []

        for d in response:
            data.append([d[0], d[1], d[2], d[3], d[4]])
    
        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response

    def delete_driver(self, search_cpf: str) -> str:
        response = self.repo.delete_driver(search_cpf)
        return response

    def driver_exists(self, search_cpf: str) -> bool:
        response = self.repo.driver_exists(search_cpf)
        return response

    def driver_is_available(self, search_cpf: str) -> bool:
        response = self.repo.driver_exists(search_cpf)
        
        if response:
            reponse = self.repo.driver_is_available(search_cpf)
        
        return response

    def get_by_cpf(self, cpf: str) -> Driver | bool:
        driver = self.repo.get_by_cpf(cpf)
        
        if driver:
            driver = Driver(
                name    = driver[0],
                cpf     = driver[1],  
                license = driver[2],  
                xp      = driver[3],
                status  = driver[4]
            )

            return driver
        
        return False

    def update_driver(
        self    : DriverController,
        name    : str,
        cpf     : str,
        license : VehicleLicense,
        xp      : int | str,
        status  : DriverStatus,
    ) -> str:
        driver = Driver(
            name    = name,
            cpf     = cpf,  
            license = license,  
            xp      = xp,
            status  = status,
        )

        return self.repo.update_driver(driver)
