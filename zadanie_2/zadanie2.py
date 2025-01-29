""" zadanie2 """
from abc import ABC, abstractmethod


class Pojazd(ABC):
    """ class represents a vehicle """

    def __init__(self, model: str, rok: int):
        """ init """
        self._model = model
        self._rok = rok
        self._predkosc = 0

    # Dokoncz definicje, rowniez setter i deleter
    @property
    def predkosc(self) -> float:
        """ velocity getter """
        return self._predkosc

    @predkosc.setter
    def predkosc(self, val: float):
        """ velocity setter """
        if val < 0:
            raise ValueError('Prędkość nie może być ujemna!')
        self._predkosc = val

    @predkosc.deleter
    def predkosc(self):
        """ velocity deleter """
        self._predkosc = 0


class Samochod(Pojazd):
    """ class represents a car """

    # w __init__ dodaj skladowa liczba_drzwi
    def __init__(self, model: str, rok: int, liczba_drzwi: int):
        """ init """
        super().__init__(model, rok)
        self.liczba_drzwi = liczba_drzwi


class Autobus(Pojazd):
    """ class represents a bus """

    # w __init__ dodaj skladowa liczba_miejsc
    def __init__(self, model: str, rok: int, liczba_miejsc: int):
        """ init """
        super().__init__(model, rok)
        self.liczba_miejsc = liczba_miejsc


class FabrykaPojazdow(ABC):
    """ abstract class represents a vehicle factory """

    def __init__(self, nazwa: str):
        """ init """
        self._nazwa = nazwa
        self._liczba_wyprodukowanych = 0

    # do uzupelnienia rozne metody jak na diagramie i w opisie
    @property
    def nazwa(self) -> str:
        """ vehicle factory name getter"""
        return self._nazwa

    @abstractmethod
    def stworz_pojazd(self, model: str, rok: int, liczba_xxx: int):
        """ create vehicle """
        return

    @classmethod
    def utworz_fabryke(cls, typ_fabryki: str, nazwa: str):
        """ create vehicle factory """
        if typ_fabryki == 'samochod':
            return FabrykaSamochodow(nazwa)
        if typ_fabryki == 'autobus':
            return FabrykaAutobusow(nazwa)
        return FabrykaPojazdow(nazwa)

    @staticmethod
    def sprawdz_rok(rok: int):
        """ check year """
        return 1900 <= rok <= 2024

    def _zwieksz_licznik(self):
        """ increment counter """
        self._liczba_wyprodukowanych += 1

    def ile_wyprodukowano(self):
        """ counter getter """
        return self._liczba_wyprodukowanych


class FabrykaSamochodow(FabrykaPojazdow):
    """ class represents a car factory """

    def stworz_pojazd(self, model: str, rok: int, liczba_drzwi: int = 4) -> Samochod:
        """ create a car """
        # tu implementacja
        if not self.sprawdz_rok(rok):
            raise ValueError('Nieprawidłowy rok produkcji!')
        self._zwieksz_licznik()
        return Samochod(model, rok, liczba_drzwi)


class FabrykaAutobusow(FabrykaPojazdow):
    """ class represents a bus factory """

    def stworz_pojazd(self, model: str, rok: int, liczba_miejsc: int = 50) -> Autobus:
        """ create a bus """
        if not self.sprawdz_rok(rok):
            raise ValueError('Nieprawidłowy rok produkcji!')
        self._zwieksz_licznik()
        return Autobus(model, rok, liczba_miejsc)


def main():
    """ main """
    # Utworz fabryki pojazdow (samochodow i autobusow)
    fabryka_samochodow = FabrykaPojazdow.utworz_fabryke('samochod', "Fabryka Samochodów Warszawa")
    fabryka_autobusow = FabrykaPojazdow.utworz_fabryke('autobus', "Fabryka Autobusów Kraków")

    # Utworzone fabryki - demonstracja @property nazwa
    print(f"Nazwa fabryki: {fabryka_samochodow.nazwa}")
    print(f"Nazwa fabryki: {fabryka_autobusow.nazwa}")

    # Utworz pojazdy
    samochod = fabryka_samochodow.stworz_pojazd("Fiat", 2023, liczba_drzwi=5)
    autobus = fabryka_autobusow.stworz_pojazd("Solaris", 2023, liczba_miejsc=60)

    # Demonstracja dzialania gettera, settera i deletera
    samochod.predkosc = 50  # uzycie setter
    print(f"Prędkość samochodu: {samochod.predkosc}")  # uzycie getter
    del samochod.predkosc  # uzycie deleter
    print(f"Prędkość po reset: {samochod.predkosc}")

    # Pokazanie ile pojazdow wyprodukowano
    print(f"Wyprodukowano samochodów: {fabryka_samochodow.ile_wyprodukowano()}")
    print(f"Wyprodukowano autobusów: {fabryka_autobusow.ile_wyprodukowano()}")


if __name__ == "__main__":
    main()
