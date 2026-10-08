import json
from vfms.config.config import file_path

class Repo():
    def __init__(
        self, 
    ):
        with open(file_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            self.database_type = settings["settings"]["repository"]
            f.close()

        self.db_path = "db/json/vehicles.json"
        