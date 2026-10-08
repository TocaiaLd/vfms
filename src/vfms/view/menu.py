from vfms.depedencies import MasterController

from vfms.view.page_vehicle import page_create_vehicle
from vfms.view.page_home import page_home

class Menu:
    def __init__(
        self, 
        master_controller       : MasterController,
        running                 : bool,
    ):
        self.master_controller  = master_controller
        self.running            = running

        while self.running:        
            page_home(self)

    def create_vehicle(self):
        request = page_create_vehicle()

        if request == False:
            return
        elif request == True:
            return self.create_vehicle()

        self.master_controller.VEHICLE_CONTROLLER.create_vehicle(request)

    # def add_maintenance(self):
    #     self.master_controller["vehicle_controller"].add_maintenance()

    def show_all_vehicles(self):
        self.controller_type.show_all_vehicles()