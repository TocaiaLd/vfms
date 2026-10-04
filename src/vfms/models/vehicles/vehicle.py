from vfms.models.maintenance import Maintenance
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.license_type import VehicleLicense

class Vehicle:
    def __init__(
        self,
        plate               : str | None,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        license_category    : VehicleLicense,
        maintenance_h       : list[Maintenance] | None
    ):
        self.plate = plate
        self.model = model
        self.brand = brand
        self.year = year
        self.mileage = mileage
        self.average_consumption = average_consumption
        self.status = status
        self.license_category = license_category
        self.maintenance_h = maintenance_h

    def __str__(self) -> str:
        return f"Plate: {self.plate}\nModel: {self.model}\nBrand: {self.brand}\nYear: {self.year}\nMileage: {self.mileage}\nAverage Consumption: {self.average_consumption}\nStatus: {self.status.name}\nLicense Category: {self.license_category.name}\nMaintenances: {self.maintenance_h}"
    
    def __repr__(self) -> str:
        return f"Vehicle(plate={self.plate}, model={self.model}, brand={self.brand}, year={self.year}, mileage={self.mileage}, average_consumption={self.average_consumption}, status={self.status.name}, license_category={self.license_category.name}), maintenances={self.maintenance_h}"

    def __eq__(self, other : Vehicle) -> bool:
        return self.plate == other.plate

    def __lt__(self, other : Vehicle) -> bool:
        return self.mileage < other.mileage

    # def __iter__(self):
        # return iter(self.maintenance_history)
            