
from collections.abc import Mapping
from math import isfinite
from typing import Any

from vfms.enums.vehicle_license import VehicleLicense


VEHICLE_TYPES = ("car", "motorcycle", "truck")
MAINTENANCE_TYPES = ("preventive", "corrective")


# Raised when the settings file contains invalid configurations.
class SettingsValidationError(ValueError):
    pass


def _validate_object(value: Any, path: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise SettingsValidationError(
            f"'{path}' must be a JSON object."
        )

    return value


def _get_required(data: Mapping, key: str, path: str) -> Any:
    if key not in data:
        raise SettingsValidationError(
            f"Missing configuration: '{path}.{key}'."
        )

    return data[key]


def _validate_number(
    value: Any,
    path: str,
    minimum: float | None = None,
    exclusive: bool = False,
) -> int | float:

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SettingsValidationError(
            f"'{path}' must be a number."
        )

    if not isfinite(value):
        raise SettingsValidationError(
            f"'{path}' must be a finite number."
        )

    if minimum is not None:
        invalid = value <= minimum if exclusive else value < minimum

        if invalid:
            raise SettingsValidationError(
                f"Invalid value for '{path}'."
            )

    return value


def validate_settings(config: dict) -> dict:
    # Validate the structure and values of settings.json.

    config = _validate_object(config, "settings")

    # Maintenance configurations
    maintenance = _validate_object(
        _get_required(config, "maintenance", "settings"),
        "maintenance"
    )

    _validate_number(
        _get_required(
            maintenance,
            "preventive_interval_km",
            "maintenance"
        ),
        "maintenance.preventive_interval_km",
        minimum=0,
        exclusive=True
    )

    costs = _validate_object(
        _get_required(
            maintenance,
            "costs_by_type",
            "maintenance"
        ),
        "maintenance.costs_by_type"
    )

    for maintenance_type in MAINTENANCE_TYPES:

        costs_by_vehicle = _validate_object(
            _get_required(
                costs,
                maintenance_type,
                "maintenance.costs_by_type"
            ),
            f"maintenance.costs_by_type.{maintenance_type}"
        )

        for vehicle_type in VEHICLE_TYPES:

            _validate_number(
                _get_required(
                    costs_by_vehicle,
                    vehicle_type,
                    f"maintenance.costs_by_type.{maintenance_type}"
                ),
                f"maintenance.costs_by_type.{maintenance_type}.{vehicle_type}",
                minimum=0
            )

    # Fuel consumption configurations
    fuel = _validate_object(
        _get_required(config, "fuel", "settings"),
        "fuel"
    )

    consumption = _validate_object(
        _get_required(
            fuel,
            "acceptable_consumption_km_per_l",
            "fuel"
        ),
        "fuel.acceptable_consumption_km_per_l"
    )

    for vehicle_type in VEHICLE_TYPES:

        limits = _validate_object(
            _get_required(
                consumption,
                vehicle_type,
                "fuel.acceptable_consumption_km_per_l"
            ),
            f"fuel.acceptable_consumption_km_per_l.{vehicle_type}"
        )

        min_value = _validate_number(
            _get_required(
                limits,
                "min",
                f"fuel.acceptable_consumption_km_per_l.{vehicle_type}"
            ),
            f"fuel.{vehicle_type}.min",
            minimum=0,
            exclusive=True
        )

        max_value = _validate_number(
            _get_required(
                limits,
                "max",
                f"fuel.acceptable_consumption_km_per_l.{vehicle_type}"
            ),
            f"fuel.{vehicle_type}.max",
            minimum=0,
            exclusive=True
        )

        if min_value > max_value:
            raise SettingsValidationError(
                f"Minimum consumption cannot exceed maximum for {vehicle_type}."
            )

    # Driver license configurations
    driver_license = _validate_object(
        _get_required(config, "driver_license", "settings"),
        "driver_license"
    )

    minimum_categories = _validate_object(
        _get_required(
            driver_license,
            "minimum_category_by_vehicle_type",
            "driver_license"
        ),
        "driver_license.minimum_category_by_vehicle_type"
    )

    for vehicle_type in VEHICLE_TYPES:

        category = _get_required(
            minimum_categories,
            vehicle_type,
            "driver_license.minimum_category_by_vehicle_type"
        )

        if (
            not isinstance(category, str)
            or category not in VehicleLicense.__members__
        ):
            raise SettingsValidationError(
                f"Invalid CNH category for {vehicle_type}: {category}"
            )

    return config




# Convert vehicle names to the keys used in settings.json.
def normalize_vehicle_type(vehicle_type: object) -> str:

    if not isinstance(vehicle_type, str):
        vehicle_type = type(vehicle_type).__name__

    aliases = {
        "car": "car",
        "cars": "car",
        "motorcycle": "motorcycle",
        "motorcycles": "motorcycle",
        "truck": "truck",
        "trucks": "truck",
    }

    vehicle_type = aliases.get(vehicle_type.lower())

    if vehicle_type is None:
        raise SettingsValidationError("Unknown vehicle type.")

    return vehicle_type


def get_maintenance_cost(
    config: dict,
    vehicle_type: str,
    maintenance_type: str | object
) -> float:

    vehicle_type = normalize_vehicle_type(vehicle_type)
    maintenance_type = getattr(maintenance_type, "value", maintenance_type)

    return config["maintenance"]["costs_by_type"][maintenance_type][vehicle_type]


def is_consumption_acceptable(
    config: dict,
    vehicle: object
) -> bool:

    vehicle_type = normalize_vehicle_type(vehicle)
    consumption = vehicle.average_consumption

    if (
        isinstance(consumption, bool)
        or not isinstance(consumption, (int, float))
        or not isfinite(consumption)
    ):
        return False

    limits = config["fuel"]["acceptable_consumption_km_per_l"][vehicle_type]

    return limits["min"] <= consumption <= limits["max"]


def is_license_compatible(
    config: dict,
    vehicle_type: str,
    driver_license: object
) -> bool:

    vehicle_type = normalize_vehicle_type(vehicle_type)

    required_category = config["driver_license"]["minimum_category_by_vehicle_type"][vehicle_type]

    if required_category not in VehicleLicense.__members__:
        return False
    driver_value = getattr(driver_license, "value", driver_license)
    if not isinstance(driver_value, str):
        return False

    if required_category == "A":
        return "A" in driver_value

    category_levels = {"B": 1, "C": 2, "D": 3, "E": 4}
    required_level = category_levels.get(required_category)
    driver_level = max(
        (category_levels.get(category, 0) for category in driver_value),
        default=0,
    )
    return required_level is not None and driver_level >= required_level
