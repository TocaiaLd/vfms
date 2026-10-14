from vfms.enums.vehicle_license import VehicleLicense
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleController:
    def __init__(self, repo):
        self.repo = repo
    
    def create_car(self, request) -> dict:
        car = Car(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            license_category    = VehicleLicense.B,
            maintenance_h       = request["maintenance_h"],
            trips               = request["trips"],
            ports               = request["ports"],
        )
       
        response = self.repo.save_vehicle(car.to_dict(), request["type"])
        return response
    
    def create_truck(self, request) -> dict:
        truck = Truck(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            license_category    = VehicleLicense.D,
            maintenance_h       = request["maintenance_h"],
            trips               = request["trips"],
            max_weight          = request["max_weight"],
            
        )
       
        response = self.repo.save_vehicle(truck.to_dict(), request["type"])
        return response
    
    def create_motorcycle(self, request) -> dict:
        motorcycle = Motorcycle(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            license_category    = VehicleLicense.A,
            maintenance_h       = request["maintenance_h"],
            trips               = request["trips"],
            cc                  = request["cc"],
        )
       
        response = self.repo.save_vehicle(motorcycle.to_dict(), request["type"])
        
        return response

    def create_vehicle(self, request) -> dict:
        response = None

        if request["type"] == "Car":
            response = self.create_car(request)
        elif request["type"] == "Truck":
            response = self.create_truck(request)
        elif request["type"] == "Motorcycle":
            response = self.create_motorcycle(request)

        return response

    def show_vehicles(self, what):
        response = self.repo.show_vehicles_json(what)

        list_of_vehicles = []

        for type, data in response.items():
            for plate, d in data.items():
                if type == "Motorcycle":
                    v = Motorcycle(
                        plate               = plate,
                        model               = d["model"],  
                        brand               = d["brand"],  
                        year                = d["year"],
                        mileage             = d["mileage"],
                        average_consumption = d["average_consumption"],
                        status              = d["status"],
                        maintenance_h       = d["maintenance_h"],
                        trips               = d["trips"],
                        cc                  = d["cc"],
                    )
                elif type == "Car":
                    v = Car(
                        plate               = plate,
                        model               = d["model"],  
                        brand               = d["brand"],  
                        year                = d["year"],
                        mileage             = d["mileage"],
                        average_consumption = d["average_consumption"],
                        status              = d["status"],
                        maintenance_h       = d["maintenance_h"],
                        trips               = d["trips"],
                        ports               = d["ports"],
                    )
                elif type == "Truck":
                    v = Truck(
                        plate               = plate,
                        model               = d["model"],  
                        brand               = d["brand"],  
                        year                = d["year"],
                        mileage             = d["mileage"],
                        average_consumption = d["average_consumption"],
                        status              = d["status"],
                        maintenance_h       = d["maintenance_h"],
                        trips               = d["trips"],
                        max_weight          = d["max_weight"],
                    )
                
                list_of_vehicles.append(v)

        return list_of_vehicles

