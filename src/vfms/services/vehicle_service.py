from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.motorcicle import Motorcicle
from vfms.models.vehicles.car import Car

from vfms.models.maintenance import Maintenance

from vfms.enums.license_type import VehicleLicense
from vfms.enums.vehicle_status import VehicleStatus


class VehicleService:
    def __init__(self, repo):
        self.repo = repo
    
    def create_vehicle(
        self,          
        type                    : str,
        plate                   : str, 
        model                   : str, 
        brand                   : str,
        year                    : int, 
        mileage                 : float,
        average_consumption     : float,
        status                  : VehicleStatus,
        license_category        : VehicleLicense,
        maintenance_h           : list[Maintenance] | None,
        ports                   : int 
    ):
        
        if type == "Car":
            vehicle = Car(
                plate,                   
                model,      
                brand,            
                year,                 
                mileage,                 
                average_consumption,
                status,
                license_category,
                maintenance_h,
                ports
            )

        self.repo.save_vehicle(vehicle, type)

    def show_all_vehicles(self):
        self.repo.show_all_vehicles()
