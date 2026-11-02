import json
from pathlib import Path

from vfms.config.settings_validations import (
    is_consumption_acceptable,
    is_license_compatible,
    validate_settings,
)
from vfms.enums.vehicle_license import VehicleLicense
from vfms.models.vehicles.car import Car
from vfms.enums.vehicle_status import VehicleStatus


def test_project_settings_require_category_c_for_trucks() -> None:
    config_path = Path(__file__).parents[1] / "src" / "vfms" / "config" / "settings.json"
    settings = validate_settings(json.loads(config_path.read_text(encoding="utf-8")))

    assert settings["driver_license"]["minimum_category_by_vehicle_type"]["truck"] == "C"


def test_license_compatibility_respects_category_levels() -> None:
    settings = {
        "driver_license": {
            "minimum_category_by_vehicle_type": {
                "car": "B", "motorcycle": "A", "truck": "C"
            }
        }
    }

    assert is_license_compatible(settings, "truck", VehicleLicense.C)
    assert is_license_compatible(settings, "truck", VehicleLicense.D)
    assert is_license_compatible(settings, "truck", VehicleLicense.E)
    assert not is_license_compatible(settings, "truck", VehicleLicense.B)
    assert is_license_compatible(settings, "motorcycle", VehicleLicense.AB)


def test_consumption_policy_uses_configured_limits() -> None:
    settings = {
        "fuel": {
            "acceptable_consumption_km_per_l": {
                "car": {"min": 8, "max": 18},
                "motorcycle": {"min": 20, "max": 45},
                "truck": {"min": 2, "max": 8},
            }
        }
    }
    car = Car("ABC-1D34", "Model", "Brand", 2020, 100, 12, VehicleStatus.AVAILABLE, 50, 0, 4)

    assert is_consumption_acceptable(settings, car)
    car.average_consumption = 20
    assert not is_consumption_acceptable(settings, car)
