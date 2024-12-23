
import threading
import tkinter as tk
import time
import turtle as tr
import cv2
import mediapipe as mp
import queue
from raket import Raket
from top import Top
from skor import Skor
from zorluk import Zorluk
from tugla import Tugla

class Main:
    @staticmethod
    def show_difficulty_selection():
        root = tk.Tk()
        root.title("Zorluk Seçimi")
        root.geometry("300x200")

        difficulty = tk.StringVar()

        def select_difficulty(value):
            difficulty.set(value)
            root.destroy()

        tk.Label(root, text="Zorluk Seçin", font=("Arial", 14)).pack(pady=10)
        tk.Button(root, text="Kolay", command=lambda: select_difficulty("kolay"), width=10).pack(pady=5)
        tk.Button(root, text="Orta", command=lambda: select_difficulty("orta"), width=10).pack(pady=5)
        tk.Button(root, text="Zor", command=lambda: select_difficulty("zor"), width=10).pack(pady=5)

        root.mainloop()
        return difficulty.get()

    @staticmethod
    def start_game(zorluk_derecesi, hareket_obj):
        ekran = tr.Screen()
        ekran.title("Atari Breakout")
        ekran.bgcolor("black")
        ekran.setup(width=1205, height=600)
        ekran.tracer(0)

        zorluk_seviyesi = Zorluk(zorluk_derecesi)
        top = Top(zorluk_derecesi)
        tugla = Tugla(zorluk_derecesi)
        tugla._duvar_yap(ekran)
        skor_tablo = Skor(zorluk_derecesi)
        oyun_raketi = hareket_obj

        def game_over():
            if skor_tablo._can == 0:
                top.goto(0, 0)
                game_over_turtle = tr.Turtle()
                game_over_turtle.hideturtle()
                game_over_turtle.speed(0)
                game_over_turtle.color("Yellow")
                game_over_turtle.penup()
                game_over_turtle.goto(0, -100)
                game_over_turtle.write(f"Kaybettiniz\nPuanınız : {skor_tablo._skor}", align="center", font=("Impact", 24, "bold"))
                time.sleep(3)
                return True
            return False

        def kazanma():
            if len(tugla._tugla_liste) == 0:
                top.penup()
                top.goto(0, 0)
                win = tr.Turtle()
                win.hideturtle()
                win.speed(0)
                win.color("Yellow")
                win.penup()
                win.goto(0, -100)
                win.write(f"Kazandınız\nPuanınız : {skor_tablo._can * skor_tablo._skor}", align="center", font=("Impact", 24, "normal"))
                time.sleep(3)
                return True
            return False

        while True:
            
            # Raketin yeni pozisyonunu hesaplama
            try:
                hareket = oyun_raketi.move_queue.get_nowait()
                x = oyun_raketi.xcor()
                yeni_x = x + hareket
                if -600 + (12 * oyun_raketi._uzunluk) < yeni_x < 600 - (12 * oyun_raketi._uzunluk):
                    oyun_raketi.setx(yeni_x)
            except queue.Empty:
                pass

            top._hareket()
            
            if game_over():
                break
            if kazanma():
                break

            top._tugla_kirma(tugla, skor_tablo)
            top._duvar_sekme(skor_tablo)
            top._raket_sekme(oyun_raketi)

            ekran.update()
            time.sleep(0.02)

if __name__ == "__main__":
    zorluk_derecesi = Main.show_difficulty_selection()

    if not zorluk_derecesi:
        print("Zorluk seviyesi seçilmedi. Program kapatılıyor.")
        exit()

    hareket_obj = Raket(zorluk_derecesi)
    
    # Amaç: Kamera hareketini ayrı bir iş parçacığında (thread) çalıştırmak.
    # Yeni bir iş parçacığı başlatır ve verilen target fonksiyonunu bu iş parçacığında çalıştırır.
    # Bu yapı, kamera işlemlerinin ana oyun döngüsünden bağımsız çalışmasını sağlar.
    camera_thread = threading.Thread(target=hareket_obj.start_camera)

    # Amaç: Yeni iş parçacığını başlatmak.
    # İş parçacığı başlatılır ve start_camera metodu arka planda çalışmaya başlar.
    # Kamera hareketleri bu iş parçacığında algılanır ve işlem yapılır.
    camera_thread.start()

    # Oyun ekranı ana iş parçacığında başlatılıyor
    Main.start_game(zorluk_derecesi, hareket_obj)

    # Amaç: Kamera iş parçacığının bitmesini beklemek.

    camera_thread.join()

