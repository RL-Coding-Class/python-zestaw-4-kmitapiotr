from functools import singledispatch, singledispatchmethod


# Singledispatch: globalna funkcja do logowania zdarzeń
@singledispatch
def log_event(event):
    raise NotImplementedError(f"Brak implementacji dla typu: {type(event)}")


# Napisz obsluge zdarzen str
@log_event.register
def _(event: str):
    return "str"


# Napisz obsluge zdarzen int
@log_event.register
def _(event: int):
    return 1


# Napisz obsluge zdarzen typu dict
@log_event.register
def _(event: dict):
    return {"python": "spanish_inquisition"}


# Klasa z metodą używającą singledispatchmethod
class EventHandler:
    def __init__(self):
        self.event_count = 0  # uwaga: licznik powiekszac o +1 przy kazdej rejestracji

    @singledispatchmethod
    def handle_event(self, event):
        """Domyślna obsługa zdarzeń"""
        raise NotImplementedError(f"Nieobsługiwany typ zdarzenia: {type(event)}")

    # Napisz obsluge zdarzen str, pamietaj: self.event_count += 1
    @handle_event.register
    def _(self, event: str):
        self.event_count += 1
        return "str"

    # Napisz obsluge zdarzen int
    @handle_event.register
    def _(self, event: int):
        self.event_count += 1
        return 1

    # Napisz obsluge zdarzen list
    @handle_event.register
    def _(self, event: list):
        self.event_count += 1
        return []


# Klasa pochodna z nowymi rejestracjami typów
class DerivedHandler(EventHandler):
    # Napisz obsluge zdarzen int
    @EventHandler.handle_event.register
    def _(self, event: int):
        self.event_count += 1
        return 2

    # Napisz obsluge zdarzen float
    @EventHandler.handle_event.register
    def _(self, event: float):
        self.event_count += 1
        return .1


# Demonstracja użycia
if __name__ == "__main__":
    # Globalna funkcja logowania zdarzeń
    print("=== Globalne logowanie zdarzeń ===")
    log_event("Uruchomienie systemu")
    log_event(404)
    log_event({"typ": "error", "opis": "Nieznany błąd"})

    # Klasa obsługująca zdarzenia
    print("\n=== Klasa EventHandler ===")
    handler = EventHandler()
    handler.handle_event("Zdarzenie logowania")
    handler.handle_event(123)
    handler.handle_event(["zdarzenie1", "zdarzenie2", "zdarzenie3"])

    # Obsługa nieobsługiwanego typu
    print("\n=== Obsługa nieobsługiwanego typu ===")
    try:
        log_event(3.14)  # Nieobsługiwany typ w log_event
    except NotImplementedError as e:
        print(e)

    try:
        handler.handle_event(set([1, 2, 3]))  # Nieobsługiwany typ w handle_event
    except NotImplementedError as e:
        print(e)

    # Klasa DerivedHandler
    print("\n=== Klasa DerivedHandler ===")
    derived_handler = DerivedHandler()
    derived_handler.handle_event("Inne zdarzenie tekstowe")
    derived_handler.handle_event(789)  # Obsługa zmieniona dla int
    derived_handler.handle_event(3.14)  # Obsługa float zarejestrowana w DerivedHandler

    # Niespodzianka: prosze sprawdzic co zobaczymy?
    handler.handle_event(12356789)
