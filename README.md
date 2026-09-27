# Vehicle Fleet Management System (vfms)

## Summary
- [Description](#description)

- [Objective](#objective)

- [Class Structure](#class-structure)

- [File Structure](#file-structure)

## Description
The vfms project is a cli program writted in python - using the oriented object programming paradigm - that allows organizations to manage they vehicle fleet.

## Objective
Learn how to use OOP and create a functional program.

## UML 
```mermaid
classDiagram

    %% ENUM
    class VehicleStatus {
        <<enumeration>>
        ACTIVE
        MAINTENANCE
        INACTIVE
    }

    %% CLASSES
    class Person {
        -_name: str
        -_cpf: str
        +name: str
        +cpf: str
    }

    class Driver {
        -_license_category: str
        -_experience: int
        -_availability: bool
        -_trip_history: list~Trip~
        +license_category: str
        +experience: int
        +availability: bool
        +trip_history: list~Trip~
        +register_trip(trip: Trip): None
    }

    class Vehicle {
        -_plate: str
        -_brand: str
        -_model: str
        -_year: int
        -_mileage: float
        -_average_consumption: float
        -_status: VehicleStatus
        +plate: str
        +brand: str
        +model: str
        +year: int
        +mileage: float
        +average_consumption: float
        +status: VehicleStatus
        +update_mileage(distance: float): None
        +change_status(status: VehicleStatus): None
        +__str__(): str
        +__repr__(): str
        +__eq__(other: object): bool
        +__lt__(other: object): bool
        +__iter__(): Iterator~Maintenance~
    }

    class Car {
    }

    class Motorcycle {
    }

    class Truck {
    }

    class FuelableMixin {
        -_refueling_history: list~Refueling~
        +refuel(refueling: Refueling): None
    }

    class MaintainableMixin {
        -_maintenance_history: list~Maintenance~
        +register_maintenance(maintenance: Maintenance): None
    }

    class Maintenance {
        -_date: date
        -_type: str
        -_cost: float
        -_description: str
    }

    class Refueling {
        -_date: date
        -_fuel_type: str
        -_liters: float
        -_amount_paid: float
    }

    class Trip {
        -_origin: str
        -_destination: str
        -_distance: float
    }

    %% INHERITANCE / INHERITS FROM MIXINS
    Person <|-- Driver
    FuelableMixin <|-- Vehicle
    MaintainableMixin <|-- Vehicle
    Vehicle <|-- Car
    Vehicle <|-- Motorcycle
    Vehicle <|-- Truck

    %% ASSOCIATIONS
    Driver "0..1" -- "0..1" Vehicle : allocation
    Vehicle "1" -- "0..*" Maintenance : has history
    Vehicle "1" -- "0..*" Refueling : has history
    Driver "1" -- "0..*" Trip : has history
    Vehicle "1" -- "0..*" Trip : participates in
```

## File Structure

```bash
vfms
│
├── pyproject.toml
├── README.md
├── src
│   └── vfms
│       ├── classes
│       │   ├── car.py
│       │   ├── driver.py
│       │   ├── maintenece_mixin.py
│       │   ├── maintenence.py
│       │   ├── motorcicle.py
│       │   ├── person.py
│       │   ├── refuel_mixin.py
│       │   ├── refuel.py
│       │   ├── trip.py
│       │   ├── truck.py
│       │   ├── vehicle.py
│       │   └── vehicle_status.py
│       ├── __init__.py
│       └── settings.json
└── uv.lock

```


