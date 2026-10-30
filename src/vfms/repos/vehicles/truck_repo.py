# Project dependencies
from vfms.models.vehicles.truck import Truck
from vfms.repos.repo import Repo

class TruckRepo():
    def __init__(
        self    : TruckRepo, 
        repo    : Repo
    ):
        self.repo = repo

    def save_truck(
        self            : TruckRepo, 
        vehicle_obj     : Truck,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo._cursor.execute("INSERT INTO trucks (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, max_weight, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.max_weight, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"

        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"
    
    def show_trucks(self) -> list:
        self.repo._cursor.execute(f"SELECT * from trucks")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles
    
    def update_truck(
        self            : TruckRepo, 
        vehicle_obj     : Truck,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if search_result:
            new_data = (vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.max_weight, vehicle_obj.license.name, vehicle_obj.plate)
            
            self.repo._cursor.execute("""
UPDATE trucks 
SET plate = ?, model = ?, brand = ?, year = ?, mileage = ?, average_consumption = ?, status = ?, max_fuel = ?, fuel = ?, max_weight = ?, license = ?  
WHERE plate = ?;
""", new_data)
            self.repo._con.commit()

            return "Vehicle updated successfuly"

        return f"Does not exists a vehicle with this plate"

    def delete_truck(self, plate) -> str:
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This truck plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM trucks WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The truck with plate {plate} was deleted."

    def get_by_plate(self, plate) -> dict:
        self.repo._cursor.execute(f"SELECT * from trucks WHERE plate = ?", (plate,))
        truck = self.repo._cursor.fetchone()

        return truck