from typing import Any
import os

# The application registry is imported by view modules; keep its test DB isolated.
os.environ["VFMS_DATABASE_PATH"] = ":memory:"

from vfms.view import menu as menu_module
from vfms.view.vehicles import menu_vehicles as vehicles_module


class Prompt:
    def __init__(self, answer: Any) -> None:
        self.answer = answer

    def ask(self) -> Any:
        return self.answer


def test_main_menu_stays_open_after_submenu_returns_none(monkeypatch: Any) -> None:
    calls = []

    def page() -> Any:
        calls.append("page")

    def close_program() -> Any:
        return False

    answers = iter([page, close_program])
    monkeypatch.setattr(menu_module.q, "select", lambda **kwargs: Prompt(next(answers)))
    monkeypatch.setattr(menu_module, "clear_screen", lambda: None)
    monkeypatch.setattr(menu_module, "close_program", close_program)

    menu_module.menu()

    assert calls == ["page"]


def test_vehicle_menu_runs_action_then_returns_to_parent(monkeypatch: Any) -> None:
    calls = []
    answers = iter([lambda: calls.append("action"), False])
    monkeypatch.setattr(vehicles_module.q, "select", lambda **kwargs: Prompt(next(answers)))
    monkeypatch.setattr(vehicles_module, "clear_screen", lambda: None)

    assert vehicles_module.menu_vehicles() is True
    assert calls == ["action"]


def test_application_registry_initializes_schema_in_isolated_database() -> None:
    from vfms.depedencies import repo

    table_names = {
        row[0]
        for row in repo.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    }
    assert {"drivers", "cars", "trucks", "motorcycles", "vehicles", "trips", "maintenances", "refuels"} <= table_names
