# Vehicle Fleet Management System (vfms)

The vfms project is a command-line application written in Python using object-oriented programming. It helps organizations manage their vehicle fleets.

## Summary

- [Description](#description)
- [Objective](#objective)
- [UML](#uml)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running](#running)
- [Data and Configuration](#data-and-configuration)
- [Classes and Architecture](#classes-and-architecture)
- [Design Decisions](#design-decisions)

## Description

The vfms project is a command-line application written in Python using object-oriented programming. It helps organizations manage vehicles, drivers, trips, refueling, and maintenance.

## Objective

Learn how to use OOP and create a functional program.

## UML

```mermaid
classDiagram
	direction TB
	class Person {
		+name: str
		+cpf: str
		-_name: str
		-_cpf: str
		+__init__(name, cpf)
		+name()
		+name(n)
		+cpf()
		+cpf(cpf)
		+__str__()
		+__repr__()
		+__eq__(other)
	}
	class Driver {
		+license: VehicleLicense
		+xp: int
		+status: DriverStatus
		-_license: VehicleLicense
		-_xp: int
		-_status: DriverStatus
		+__init__(name, cpf, license, xp, status)
		+license()
		+license(value)
		+xp()
		+xp(value)
		+status()
		+status(value)
		+__str__()
		+__repr__()
		+__lt__(other)
		+__iter__()
	}
	class Vehicle {
		<<base>>
		+plate: str
		+model: str
		+brand: str
		+year: int
		+mileage: float
		+average_consumption: float
		+status: VehicleStatus
		+max_fuel: float
		+fuel: float
		-_plate: str
		-_year: int
		-_mileage: float
		-_average_consumption: float
		-_status: VehicleStatus
		-_max_fuel: float
		-_fuel: float
		+__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
		+plate()
		+plate(p)
		+mileage()
		+mileage(value)
		+year()
		+year(value)
		+average_consumption()
		+average_consumption(value)
		+fuel()
		+fuel(value)
		+max_fuel()
		+max_fuel(value)
		+status()
		+status(value)
		+to_dict()
		+__str__()
		+__repr__()
		+__eq__(other)
		+__lt__(other)
	}
	class Car {
		+ports: int
		+license: VehicleLicense
		-_ports: int
		+__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, ports, license)
		+ports()
		+ports(value)
		+to_dict()
		+__str__()
		+__repr__()
	}
	class Motorcycle {
		+cc: int
		+license: VehicleLicense
		-_cc: int
		+__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, cc, license)
		+cc()
		+cc(value)
		+to_dict()
		+__str__()
		+__repr__()
	}
	class Truck {
		+max_weight: float
		+license: VehicleLicense
		-_max_weight: float
		+__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, max_weight, license)
		+max_weight()
		+max_weight(value)
		+to_dict()
		+__str__()
		+__repr__()
	}
	class Trip {
		+driver_cpf: str
		+vehicle_plate: str
		+origin: str
		+destiny: str
		+distance: float
		+status: EnumTrip
		+date_init: datetime
		+date_end: datetime
		-_status: EnumTrip
		+__init__(driver_cpf, vehicle_plate, origin, destiny, distance, status)
		+status()
		+status(value)
		+set_date_init()
		+set_date_end()
	}
	class RefuelMixin {
		+fuel: float
		+refuel(liters, price_per_liter)
	}
	class MaintenanceMixin {
		+type: EnumMaintenance
		+price: float
		+description: str
		+date_init: str
		+date_end: str
		+new_maintenance(type, price, description, date)
	}
	class VehicleStatus {
		<<enumeration>>
		AVAILABLE
		INACTIVE
		ON_TRIP
		MAINTENANCE
	}
	class DriverStatus {
		<<enumeration>>
		AVAILABLE
		ON_TRIP
		INACTIVE
	}
	class EnumTrip {
		<<enumeration>>
		IN_PROGRESS
		ENDED
	}
	class EnumMaintenance {
		<<enumeration>>
		PREVENTIVE
		CORRECTIVE
	}
	class VehicleLicense {
		<<enumeration>>
		A
		B
		D
		AB
		AD
	}

	Person <|-- Driver
	RefuelMixin <|-- Vehicle
	MaintenanceMixin <|-- Vehicle
	Vehicle <|-- Car
	Vehicle <|-- Motorcycle
	Vehicle <|-- Truck
	Driver --> DriverStatus
	Driver --> VehicleLicense
	Driver ..> Trip : trip_history
	Vehicle --> VehicleStatus
	Car --> VehicleLicense
	Motorcycle --> VehicleLicense
	Truck --> VehicleLicense
	Trip --> EnumTrip
	Trip ..> Driver : driver_cpf
	Trip ..> Vehicle : vehicle_plate
	MaintenanceMixin ..> EnumMaintenance

	class DriverController {
		+repo: DriverRepo
		+__init__(repo)
		+new_driver(request)
		+show_drivers()
		+show_driver_by_cpf(search_cpf)
		+delete_driver(search_cpf)
		+driver_exists(search_cpf)
		+driver_is_available(search_cpf)
		+get_by_cpf(cpf)
		+update_driver(name, cpf, license, xp, status)
	}
	class TripController {
		+repo: TripRepo
		+__init__(repo)
		+new_trip(request)
		+get_trip_by_id(trip_id)
		+finish_trip(trip_id)
		+show_trips()
	}
	class MaintenanceController {
		+repo: MaintenanceRepo
		+__init__(repo)
		+save_maintenance(maintenance)
		+show_maintenances()
		+get_maintenance_by_id(maintenance_id)
		+finish_maintenance(maintenance_id)
	}
	class RefuelController {
		+repo: RefuelRepo
		+__init__(repo)
		+save_refuel(refuel)
	}
	class CarController {
		+repo: CarRepo
		+__init__(repo)
		+create_car(request)
		+show_cars()
		+get_by_plate(plate)
		+update_car(car_obj)
		+delete_car(plate)
		+refuel_car(plate_to_refuel, liters, price_per_liter)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
		+add_maintenance(plate_to_add_maintenance, type_maintenance, price, description)
	}
	class MotorcycleController {
		+repo: MotorcycleRepo
		+__init__(repo)
		+create_motorcycle(request)
		+show_motorcycles()
		+get_by_plate(plate)
		+update_motorcycle(motorcycle_obj)
		+delete_motorcycle(plate)
		+refuel_motorcycle(plate_to_refuel, liters, price_per_liter)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
		+add_maintenance(plate_to_add_maintenance, type_maintenance, price, description)
	}
	class TruckController {
		+repo: TruckRepo
		+__init__(repo)
		+create_truck(request)
		+show_trucks()
		+get_by_plate(plate)
		+update_truck(truck_obj)
		+delete_truck(plate)
		+refuel_truck(plate_to_refuel, liters, price_per_liter)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
		+add_maintenance(plate_to_add_maintenance, type_maintenance, price, description)
	}
	class DriverRepo {
		+repo: Repo
		+__init__(repo)
		+save_driver(driver)
		+read_drivers()
		+read_driver_by_cpf(search_cpf)
		+delete_driver(search_cpf)
		+driver_exists(search_cpf)
		+driver_is_available(search_cpf)
		+get_by_cpf(cpf)
		+update_driver(driver)
	}
	class TripRepo {
		+repo: Repo
		+__init__(repo)
		+save_trip(trip)
		+finish_trip(trip, trip_id)
		+get_trip_by_id(trip_id)
		+read_trips()
	}
	class MaintenanceRepo {
		+repo: Repo
		+__init__(repo)
		+save_maintenance(maintenance)
		+read_maintenances()
		+get_maintenance_by_id(maintenance_id)
		+finish_maintenance(vehicle_plate, maintenance_id)
	}
	class RefuelRepo {
		+repo: Repo
		+__init__(repo)
		+save_refuel(maintenance)
	}
	class CarRepo {
		+repo: Repo
		+__init__(repo)
		+save_car(vehicle_obj)
		+show_cars()
		+update_car(vehicle_obj)
		+delete_car(plate)
		+get_by_plate(plate)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
	}
	class MotorcycleRepo {
		+repo: Repo
		+__init__(repo)
		+save_motorcycle(vehicle_obj)
		+show_motorcycles()
		+update_motorcycle(vehicle_obj)
		+delete_motorcycle(plate)
		+get_by_plate(plate)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
	}
	class TruckRepo {
		+repo: Repo
		+__init__(repo)
		+save_truck(vehicle_obj)
		+show_trucks()
		+update_truck(vehicle_obj)
		+delete_truck(plate)
		+get_by_plate(plate)
		+vehicle_exists(search_plate)
		+vehicle_is_available(search_plate)
	}
	class Repo {
		-_con: sqlite3.Connection
		-_cursor: sqlite3.Cursor
		+__init__()
		+create_cars_table()
		+create_trucks_table()
		+create_motorcycles_table()
		+create_drivers_table()
		+create_trips_table()
		+create_vehicles_table()
		+create_vehicles_table_triggers()
		+create_maintenances_table()
		+create_refuels_table()
	}
	class MasterController {
		<<registry>>
		+CAR_CONTROLLER
		+TRUCK_CONTROLLER
		+MOTORCYCLE_CONTROLLER
		+DRIVER_CONTROLLER
		+REFUEL_CONTROLLER
		+TRIP_CONTROLLER
		+MAINTENANCE_CONTROLLER
	}
	class SettingsValidationError {
	}

	DriverController --> DriverRepo
	TripController --> TripRepo
	MaintenanceController --> MaintenanceRepo
	RefuelController --> RefuelRepo
	CarController --> CarRepo
	MotorcycleController --> MotorcycleRepo
	TruckController --> TruckRepo
	DriverController ..> Driver
	TripController ..> Trip
	CarController ..> Car
	MotorcycleController ..> Motorcycle
	TruckController ..> Truck
	DriverRepo --> Repo
	TripRepo --> Repo
	MaintenanceRepo --> Repo
	RefuelRepo --> Repo
	CarRepo --> Repo
	MotorcycleRepo --> Repo
	TruckRepo --> Repo
	DriverRepo ..> Driver
	TripRepo ..> Trip
	MasterController ..> DriverController
	MasterController ..> TripController
	MasterController ..> MaintenanceController
	MasterController ..> RefuelController
	MasterController ..> CarController
	MasterController ..> MotorcycleController
	MasterController ..> TruckController
```

## File Structure

```text
src/vfms/controllers/  Coordinate application operations
src/vfms/models/       Domain objects and shared behaviors
src/vfms/repos/        SQLite persistence
src/vfms/view/         Interactive terminal menus
src/vfms/enums/        Status, maintenance, trip, and license values
src/vfms/config/       Application settings and validation
db/                    Local SQLite database
docs/                  Additional project documentation
```

## Requirements

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

Install `uv` if needed:

```bash
# Linux and macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/TocaiaLd/vfms.git
cd vfms
uv sync
```

## Running

```bash
uv run vfms
```

Use the arrow keys to navigate menus and press Enter to select an option. Follow the prompts to add or update records. Use the back option in a menu to return to the previous screen.

### Main Menu

- **Vehicles:** create, list, update, delete, or refuel cars, motorcycles, and trucks.
- **Drivers:** register, list, search by CPF, update, or delete drivers.
- **Trips:** create, list, or finish trips. Select an available driver and vehicle, then enter the trip details. A compatible driver's license is required.
- **Maintenances:** list, add, or finish vehicle maintenance records.

## Data and Configuration

The application creates and uses `db/sqlite3.db` for local data. The database schema is initialized when the application starts. Settings in `src/vfms/config/settings.json` define preventive maintenance intervals and reference costs, acceptable fuel-consumption ranges, and minimum license categories.

## Classes and Architecture

| Area | Classes | Responsibility |
| --- | --- | --- |
| People | `Person`, `Driver` | `Person` provides shared identity data; `Driver` adds license, experience, status, and trip history. |
| Vehicles | `Vehicle`, `Car`, `Motorcycle`, `Truck` | `Vehicle` contains shared vehicle attributes and validation; each subclass adds its type-specific data. `Vehicle` also uses `RefuelMixin` and `MaintenanceMixin`. |
| Operations | `Trip` | Stores trip details, status, and start/end dates. |
| Shared behavior | `RefuelMixin`, `MaintenanceMixin` | Provide refueling and maintenance-record operations to vehicle models. |
| Controllers | `DriverController`, `TripController`, `MaintenanceController`, `RefuelController`, `CarController`, `MotorcycleController`, `TruckController` | Coordinate user-facing operations between models and repositories. |
| Repositories | `Repo`, `DriverRepo`, `TripRepo`, `MaintenanceRepo`, `RefuelRepo`, `CarRepo`, `MotorcycleRepo`, `TruckRepo` | `Repo` owns the SQLite connection and schema; specialized repositories persist each domain area. |
| Shared values | `VehicleStatus`, `DriverStatus`, `EnumTrip`, `EnumMaintenance`, `VehicleLicense` | Enumerate supported states, maintenance types, trip states, and license categories. |
| Application wiring | `MasterController` | Provides the shared controller instances used by the terminal views. |
| Configuration | `SettingsValidationError` | Reports invalid application settings loaded from JSON. |

## Design Decisions

- Inheritance keeps shared person and vehicle attributes in base classes, while vehicle subclasses contain only type-specific fields.
- Mixins provide refueling and maintenance behavior that is shared across vehicle types.
- Views, controllers, models, and repositories have separate responsibilities, keeping terminal interaction apart from persistence and domain behavior.
- Enums represent finite states and categories instead of relying on arbitrary strings throughout the application.
- SQLite keeps data local without requiring a separate database server. Vehicle-specific tables are synchronized with the shared `vehicles` table using SQLite triggers.
- JSON settings make maintenance intervals, reference costs, fuel ranges, and license requirements configurable; the settings module validates them at startup.


