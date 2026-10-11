class Trip:
    """Representa uma viagem realizada por um motorista e um veículo."""
    def __init__(
        self        : Trip,
        origin      : str,
        destiny     : str,
        distance    : float,
    ):
        self.origin     = origin
        self.destiny    = destiny
        self.distance   = distance