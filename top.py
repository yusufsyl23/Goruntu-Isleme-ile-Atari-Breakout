from turtle import Turtle
from zorluk import Zorluk
import time

class Top(Turtle,Zorluk):
    def __init__(self,zorluk_derecesi):
    
        Turtle.__init__(self)
        Zorluk.__init__(self,zorluk_derecesi)
        
        self.shape("circle")
        self.shapesize(stretch_wid = self._boyut, stretch_len = self._boyut)
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(0,0)
    
    def _hareket(self):
        self.setx(self.xcor() + self._dx)
        self.sety(self.ycor() + self._dy)

    def _raket_sekme(self,oyun_raketi):
        if (self.ycor() <= -225 and self.ycor() >= -235) and (self.xcor() <= oyun_raketi.xcor() + self._uzunluk*10 and self.xcor() >= oyun_raketi.xcor() - self._uzunluk*10):
            self.sety(-225)
            self._dy *= -1
    
    def _duvar_sekme(self,skor_tablo):
        if (self.xcor() > 600 - self._boyut * 10):
            self.setx(600 - self._boyut * 10)
            self._dx *= -1
        
        if (self.xcor() < (600 - self._boyut * 10)*-1):    
            self.setx((600 - self._boyut * 10)*-1)       
            self._dx *= -1

        if (self.ycor() > 280 - self._boyut * 10):
            self.sety(280 - self._boyut * 10)
            self._dy *= -1

        if (self.ycor() < (290 - self._boyut * 10) * -1):
            self.sety((290 - self._boyut * 10) * -1)
            time.sleep(1)
            skor_tablo._can_azalt()
            self.goto(0,0)
            self._dx *= -1

    def _tugla_kirma(self, tugla, skor_tablo):
        for i in tugla._tugla_liste:
            tuğla_yukseklik = i.shapesize()[1] * 20  # Yükseklik değerini şekil boyutundan al
            tuğla_genislik = i.shapesize()[0] * 20  # Genişlik değerini şekil boyutundan al
            top_yaricap = self._boyut * 10

            if (i.ycor() - tuğla_yukseklik / 2 < self.ycor() + top_yaricap < i.ycor() + tuğla_yukseklik / 2) and \
            (i.xcor() - tuğla_genislik / 2 < self.xcor() + top_yaricap < i.xcor() + tuğla_genislik / 2):
                i.hideturtle()
                tugla._tugla_liste.remove(i)
                skor_tablo._skor_artis()
                self._dy *= -1

    
    

    



        

    
        

         


