from vfms.enums.vehicle_status import VehicleStatus
from vfms.models.vehicles.car import Car

c = Car(
        plate               = "ABC-1D34",
        model               = "Onix",
        brand               = "Chevrolet",
        year                = 2020,
        mileage             = 10000.0,
        average_consumption = 10.0,
        status              = VehicleStatus.AVAILABLE,
        trips               = [],
        maintenance_h       = [],
        ports               = 4,
    )

print(c.to_dict())