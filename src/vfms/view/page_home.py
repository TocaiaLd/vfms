from vfms.view.page_close import page_close
from questionary import questionary

def page_home(menu):
    question = "Choose a option:"

    options = [
        questionary.Choice("New vehicle", value=menu.create_vehicle), 
        questionary.Choice("Print all vehicles", value=menu.show_all_vehicles), 
        # questionary.Choice("Add a maintenance to one vehicle", value=menu.add_maintenance), 
        questionary.Choice("Close Program", value=0), 
    ]
            
    input = questionary.select(
        question,
        choices=options
    ).ask()

    if input == 0:
        menu.running = page_close(message="Are you sure to close the program?")
        return
    
    input()
