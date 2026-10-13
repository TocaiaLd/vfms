# standard libs
from pathlib import Path
import json

# external libs
import questionary as q

file_path = "src/vfms/config/settings.json"

databases_choices = ["json", "sqlite3"]

settings_dict = {
    "settings": {
        "repository": "",
    }
}

def first_inicialization():
    q.print("It's the first time using the program. Inicializing the settings.json file...")
    
    database = q.select(
        "Select the database",
        choices = databases_choices
    ).ask()

    settings_dict["settings"]["repository"] = database

    if database == "json":
        settings_dict["settings"]["last_id_trip"] = 0
        
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4, ensure_ascii=False)
        f.close()

def verify_integrity() -> bool:
    with open(file_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

        for item in databases_choices:
            settings_dict["settings"]["repository"] = item

            if settings["settings"]["repository"] == settings_dict["settings"]["repository"]:
                return True

        q.print("settings.json is in a wrong format, recreating settings...")
        return False


def check_config() -> None:
    file = Path(file_path)
    
    if not file.is_file() or not verify_integrity():
        first_inicialization()
    