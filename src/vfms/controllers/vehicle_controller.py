
class VehicleController:
    def __init__(self, service):
        self.service = service
    
    def create_car(self, request):
        self.service.create_vehicle(
            request["type"],
            request["plate"],
            request["model"],
            request["brand"],
            request["year"],
            request["mileage"],
            request["average_consumption"],
            request["status"],
            request["license_category"],
            request["maintenance_h"],
            request["ports"],
        )
    
    def create_truck(self, request):
        self.service.create_vehicle(
            request["type"],
            request["plate"],
            request["model"],
            request["brand"],
            request["year"],
            request["mileage"],
            request["average_consumption"],
            request["status"],
            request["license_category"],
            request["maintenance_h"]
        )
    
    def create_motorcicle(self, request):
        self.service.create_vehicle(
            request["type"],
            request["plate"],
            request["model"],
            request["brand"],
            request["year"],
            request["mileage"],
            request["average_consumption"],
            request["status"],
            request["license_category"],
            request["maintenance_h"]
        )

    def create_vehicle(self, request):
        if request["type"] == "Car":
            self.create_car(request)
        elif request["type"] == "Truck":
            self.create_truck(request)
        elif request["type"] == "Motorcicle":
            self.create_motorcicle(request)

    def show_all_vehicles(self):
        self.service.show_all_vehicles()