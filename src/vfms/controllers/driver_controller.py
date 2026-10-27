# Projects imports
from vfms.models.users.driver import Driver

class DriverController:
    def __init__(self, repo):
        self.repo = repo
    
    def new_driver(self, request):
        driver = Driver(
            name            = request["name"],
            cpf             = request["cpf"],
            license         = request["license"],
            xp              = request["xp"],
            status          = request["status"],
            trip_history    = request["trip_history"]
        )

        self.repo.save_driver(driver)

    def show_drivers(self):
        response = self.repo.read_drivers()

        list_of_drivers = []

        for cpf, data in response.items():
            driver = Driver(
                name            = data["name"],
                cpf             = cpf,
                license         = data["license"],
                xp              = data["xp"],
                status          = data["status"],
                trip_history    = data["trip_history"]
            )
            
            list_of_drivers.append(driver)

        return list_of_drivers
    
    def show_driver_by_cpf(self, search_cpf):
        response = self.repo.read_driver_by_cpf(search_cpf)

        driver = None

        if response:
            for cpf, data in response.items():
                driver = Driver(
                    name            = data["name"],
                    cpf             = cpf,
                    license         = data["license"],
                    xp              = data["xp"],
                    status          = data["status"],
                    trip_history    = data["trip_history"]
                )
            
        return driver