# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo

class DriverRepo(Repo):
    def __init__(
        self, 
    ):
        super().__init__()
    
    def save_driver(
            self, 
            driver,
        ):
        
        if self.database_type == "json":
            self.save_driver_json(driver)
        else:
            self.save_driver_sql(driver)

    def save_driver_json(self, driver):
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            new_item = {
                "name"            : driver.name,
                "license"         : driver.license.name,
                "xp"              : driver.xp,
                "status"          : driver.status.name,
                "trip_history"    : driver.trip_history
            }

            database[driver.cpf] = new_item
            f.close()

        with open(self.db_driver_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()
        
        print(f"Driver {driver.name} saved! Returning to menu...")

    def save_driver_sql(self, vehicl):
        pass

    def read_drivers_json(self):
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            database = json.load(f)

        list_drivers = {}

    
        for cpf, data in database.items():
            list_drivers[cpf] = data

        return list_drivers

    def read_driver_by_cpf(self, search_cpf):
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            database = json.load(f)

        searched_driver = {}


        for cpf, data in database.items():
            if cpf == search_cpf:
                searched_driver[cpf] = data

        return searched_driver


