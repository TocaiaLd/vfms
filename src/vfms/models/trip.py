class Trip:
    """Representa uma viagem realizada por um motorista e um veículo."""
    def __init__(
        self            : Trip,
        driver_cpf      : str,
        vehicle_plate   : str,
        origin          : str,
        destiny         : str,
        distance        : float,
    ):
        self.driver_cpf     = driver_cpf
        self.vehicle_plate  = vehicle_plate
        self.origin         = origin
        self.destiny        = destiny
        self.distance       = distance
