# Standard imports
from datetime import datetime
from math import isfinite

class RefuelMixin:
    # Apply fuel purchases to objects exposing fuel and tank capacity.
    def refuel(
        self            : RefuelMixin,
        liters          : float | str,
        price_per_liter : float | str,
    ) -> tuple[str | None, float, float, float, datetime] | None:
        date = datetime.now()
        n_liters = float(liters)
        n_price_per_liter = float(price_per_liter)

        if not isfinite(n_liters) or not isfinite(n_price_per_liter):
            raise ValueError("Liters and price per liter must be finite numbers")

        if n_liters <= 0:
            print("[Erro] Não é possível abastecer uma quantidade menor ou igual a zero.")
            return None
        if n_price_per_liter < 0:
            raise ValueError("O preço por litro não pode ser negativo")

        fuel        = getattr(self, 'fuel', 0.0)
        max_fuel    = getattr(self, 'max_fuel', float('inf'))
        vehicle_plate= getattr(self, 'plate', None)

        if fuel + n_liters > max_fuel:
            liters_allowed = max_fuel - fuel
            print(f"[Aviso] {n_liters}L excede a capacidade. Abastecendo apenas {liters_allowed:.2f}L para encher o tanque.")
            n_liters = liters_allowed

        if n_liters <= 0:
            print("[Erro] Não é possível abastecer uma quantidade menor ou igual a zero.")
            return None

        self.fuel = fuel + n_liters
        total_cost= n_liters * n_price_per_liter
        total_cost      = round(total_cost, 2)

        # Cria o registro do abastecimento
        record = (vehicle_plate, n_liters, n_price_per_liter, total_cost, date)
        
        print(f"[Mixin] Abastecido com sucesso! Nível atual do tanque: {self.fuel}L")

        return record
