from vfms.view.page_vehicle import page_create_vehicle
from vfms.view.page_home import page_home
import os

class Menu:
    def __init__(
        self, 
        master_controller       : list,
        running                 : bool,
        message                 : str = "",
    ):
        self.master_controller  = master_controller
        self.running            = running
        self.message            = message

        while self.running:        
            page_home(self)
            
            # os.name == 'nt' and os.system('cls') or os.system('clear')

    def create_vehicle(self):
        request = page_create_vehicle()

        if request == False:
            return
        elif request == True:
            return self.create_vehicle()

        self.master_controller["vehicle_controller"].create_vehicle(request)

    def add_maintenance(self):
        self.master_controller["vehicle_controller"].add_maintenance(request)

    def show_all_vehicles(self):
        self.controller_type.show_all_vehicles()