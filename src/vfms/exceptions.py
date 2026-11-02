# Application exceptions for business and persistence failures.


class ManutencaoInvalidaError(ValueError):
    # Raised when a maintenance operation has invalid data or state.
    pass


class AlocacaoInvalidaError(ValueError):
    # Raised when a driver or vehicle cannot be assigned to a trip.
    pass


class PoliticaNaoAtendidaError(ValueError):
    # Raised when an operation violates a configured application policy.
    pass


class RepositorioError(RuntimeError):
    # Raised when a repository operation fails in SQLite.
    pass
