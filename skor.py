from turtle import Turtle
from zorluk import Zorluk

class Skor(Turtle,Zorluk):
    def __init__(self,zorluk_derecesi):

        Turtle.__init__(self)
        Zorluk.__init__(self,zorluk_derecesi)
        self._skor = 0
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-450,250)
        self.__skor_guncelle()
        
    def __skor_guncelle(self):
        self.clear()
        self.write(f"Skor : {self._skor}     Can : {self._can}", align = "center" , font = ('arial', 18, 'normal'))

    def _can_azalt(self):
        self._can -= 1
        self.__skor_guncelle()

    def _skor_artis(self):
        self._skor += self._artis
        self.__skor_guncelle()
