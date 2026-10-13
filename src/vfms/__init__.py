from vfms.config.settings import check_config
from vfms.view.page_home import menu

def main() -> None:
    check_config()
    menu()
