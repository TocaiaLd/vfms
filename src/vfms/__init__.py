from vfms.view.menu import Menu
from vfms.depedencies import master_controller

def main() -> None:
    menu = Menu(master_controller, True)

