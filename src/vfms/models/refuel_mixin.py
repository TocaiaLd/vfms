# Standard imports
from datetime import datetime

class RefuelMixin:
    def refuel(
        self            : RefuelMixin,
        liters          : float,
        price_per_liter : float,
    ) -> tuple:
        date = datetime.now()
        n_liters = float(liters)

        fuel        = getattr(self, 'fuel', 0.0)
        max_fuel    = getattr(self, 'max_fuel', float('inf'))
        vehicle_plate= getattr(self, 'plate', None)

        if fuel + n_liters > max_fuel:
            liters_allowed = max_fuel - fuel
            print(f"[Aviso] {n_liters}L excede a capacidade. Abastecendo apenas {liters_allowed:.2f}L para encher o tanque.")
            n_liters = liters_allowed

        if n_liters <= 0:
            print("[Erro] Não é possível abastecer uma quantidade menor ou igual a zero.")
            return

        self.fuel = fuel + n_liters
        total_cost= n_liters * float(price_per_liter)
        total_cost      = round(total_cost, 2)

        # Cria o registro do abastecimento
        record = (vehicle_plate, n_liters, float(price_per_liter), total_cost, date)
        
        print(f"[Mixin] Abastecido com sucesso! Nível atual do tanque: {self.fuel}L")

        return record
