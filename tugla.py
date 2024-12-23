import turtle
import random
from zorluk import Zorluk

class Tugla(Zorluk):

    def __init__(self,zorluk_derecesi):
        super().__init__(zorluk_derecesi)
        self._tugla_liste = []

    def __tugla_yap(self, x, y):
        renkler = ['light blue', 'royal blue', 'light steel blue', 'steel blue', 'light cyan', 'light sky blue',
                   'violet', 'salmon', 'tomato', 'sandy brown', 'purple', 'deep pink', 'medium sea green', 'khaki']
        tugla = turtle.Turtle()
        tugla.shape("square")
        tugla.color(random.choice(renkler))
        tugla.pencolor("black")
        tugla.shapesize(self._tugla_boyut[0], self._tugla_boyut[1])  
        tugla.penup()
        tugla.goto(x, y)
        return tugla
    
    
    def _duvar_yap(self, ekran):
        ekran_genisligi = ekran.window_width()
        tugla_genislik = self._tugla_boyut[1] * 20
        bas_x = -(ekran_genisligi // 2) + (tugla_genislik // 2)

        for y in range(100, 250, int(self._tugla_boyut[0] * 20)):
            for x in range(bas_x, ekran_genisligi // 2 - tugla_genislik // 2,int(tugla_genislik)):
                tugla = self.__tugla_yap(x, y)
                self._tugla_liste.append(tugla)
