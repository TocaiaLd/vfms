import questionary as q

def close_program() -> bool:
    sure = q.confirm("Are you sure to close the program?").ask()

    return not sure
    
