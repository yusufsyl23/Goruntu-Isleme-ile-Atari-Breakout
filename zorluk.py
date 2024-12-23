import tkinter as tk

class Zorluk:
    def __init__(self, zorluk_derecesi):
        self.zorluk_derecesi = zorluk_derecesi

        if self.zorluk_derecesi == "kolay":
            self._can = 100
            self._dx = -3
            self._dy = -3
            self._uzunluk = 9
            self._boyut = 2
            self._artis = 5
            self._tugla_boyut = (2, 4)

        elif self.zorluk_derecesi == "orta":
            self._can = 3
            self._dx = -5
            self._dy = -5
            self._uzunluk = 7
            self._boyut = 1
            self._artis = 10
            self._tugla_boyut = (1.5, 3)

        elif self.zorluk_derecesi == "zor":
            self._can = 1
            self._dx = -7
            self._dy = -7
            self._uzunluk = 5
            self._boyut = 0.5
            self._artis = 15
            self._tugla_boyut = (1, 2)

    def get_params(self):
        return {
            "can": self._can,
            "dx": self._dx,
            "dy": self._dy,
            "uzunluk": self._uzunluk,
            "boyut": self._boyut,
            "artis": self._artis,
            "tugla_boyut": self._tugla_boyut
        }
