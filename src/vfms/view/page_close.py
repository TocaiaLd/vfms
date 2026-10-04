import questionary

def page_close(message : str) -> bool:
    sure = questionary.confirm(message).ask()
    if sure:
        return False
    else:
        return True
