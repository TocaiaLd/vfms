from vfms.config.config import check_config
from vfms.view.menu import Menu
from vfms.depedencies import MasterController

def main() -> None:
    check_config()
    menu = Menu(
        master_controller=MasterController, 
        running=True
    )

