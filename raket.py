from turtle import Turtle
from zorluk import Zorluk
import cv2
import queue
import mediapipe as mp


class Raket(Turtle, Zorluk):
    def __init__(self, zorluk_derecesi):
        Turtle.__init__(self)
        Zorluk.__init__(self, zorluk_derecesi)
        self.speed(0)
        self.shape("square")
        self.shapesize(stretch_len=self._uzunluk, stretch_wid=1)
        self.color("white")
        self.penup()
        self.goto(0, -250)

        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.mp_draw = mp.solutions.drawing_utils
        self.move_queue = queue.Queue()
    
    def process_hand_movement(self, hand_data):
    # Hem sağ hem sol el varsa
        if "Right" in hand_data and "Left" in hand_data:
            right_thumb_tip = hand_data["Right"].landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            right_thumb_ip = hand_data["Right"].landmark[mp.solutions.hands.HandLandmark.THUMB_IP]

            left_thumb_tip = hand_data["Left"].landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            left_thumb_ip = hand_data["Left"].landmark[mp.solutions.hands.HandLandmark.THUMB_IP]

            # Her iki başparmak da açık mı? (Yukarıda mı?)
            if right_thumb_tip.y < right_thumb_ip.y and left_thumb_tip.y < left_thumb_ip.y:
                # Her iki başparmak yukarıdaysa hareket etme
                return "Hareketsiz"

            # Sağ başparmak yukarıdaysa sağa hareket
            if right_thumb_tip.y < right_thumb_ip.y:
                self.move_queue.put(20)  # Sağa hareket
                return "Sağa Hareket"

            # Sol başparmak yukarıdaysa sola hareket
            if left_thumb_tip.y < left_thumb_ip.y:
                self.move_queue.put(-20)  # Sola hareket
                return "Sola Hareket"

        return None

    def start_camera(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks and results.multi_handedness:
                hand_data = {}
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Sağ veya sol el ayrımı
                    label = handedness.classification[0].label  # "Right" veya "Left"
                    hand_data[label] = hand_landmarks

                    # El işaretlerini çizin
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                # El hareketini işleme
                action = self.process_hand_movement(hand_data)
                if action:
                    cv2.putText(frame, action, (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            cv2.imshow("Hareket", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC ile çıkış
                break

        self.cap.release()
        cv2.destroyAllWindows()


