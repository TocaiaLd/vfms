# standard libs
from pathlib import Path
import json

# external libs
import questionary as q

# Settings file path
file_path = "src/vfms/config/settings.json"

def json_configuration() -> dict:
    drivers_json_path   = Path("db/json/drivers.json")
    vehicles_json_path  = Path("db/json/vehicles.json")
    trips_json_path     = Path("db/json/trips.json")
    
    settings_dict = {
        "settings": {
            "repository"    : "json",
            "files"         : [
                "drivers.json",
                "trips.json",
                "vehicles.json"
            ],
            "last_id_trip"  : 0
        }
    }

    if not drivers_json_path.is_file():
        drivers_dict = {}

        with open(drivers_json_path, "w", encoding="utf-8") as f:
            json.dump(drivers_dict, f, indent=4, ensure_ascii=False)
            f.close()

    if not trips_json_path.is_file():
        trips_dict = {}

        with open(trips_json_path, "w", encoding="utf-8") as f:
            json.dump(trips_dict, f, indent=4, ensure_ascii=False)
            f.close()
    if not vehicles_json_path.is_file():
        vehicles_dict = {
            "Car"           : {},
            "Truck"         : {},
            "Motorcycle"    : {}
        }

        with open(vehicles_json_path, "w", encoding="utf-8") as f:
            json.dump(vehicles_dict, f, indent=4, ensure_ascii=False)
            f.close()

    return settings_dict

def sqlite3_configuration() -> dict:
    pass

# Databases to choose
databases_choices = [
    q.Choice(title="json", value=json_configuration)
]

def first_inicialization() -> bool:
    q.print("It's the first time using the program. Inicializing the settings.json file...")
    
    database = q.select(
        "Select the database",
        choices = databases_choices
    ).ask()

    settings_dict = database()
        
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4, ensure_ascii=False)
        f.close()

def check_config() -> None:
    file = Path(file_path)
    
    if not file.is_file():
        first_inicialization()
    