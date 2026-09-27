from enum import Enum

class VehicleStatus(Enum):
    """Representa os estados possíveis de um veículo."""

    ACTIVE = "ativo"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"