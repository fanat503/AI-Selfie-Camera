import cv2
import mediapipe as mp
import math
import threading
import pyautogui # Библиотека для нажатия кнопок
import time      # Библиотека для работы со временем

# --- ЭТОТ КЛАСС УБИРАЕТ ЛАГИ (Оставляем как было) ---
class ThreadedCamera:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status = False
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            
    def get_frame(self):
        return self.status, self.frame

# --- НАСТРОЙКИ ---

# 1. ВПИШИ СВОЙ IP С ТЕЛЕФОНА
address = "http://192.168.100.7:8080/video"

# 2. Настройки времени
last_click_time = 0   # Когда было последнее нажатие
cooldown = 1.0        # Задержка в секундах (чтобы не спамить пробелом)
    
try:
    cap = ThreadedCamera(address)
except:
    print("Ошибка подключения! Проверь IP.")
    exit()

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)    

print("Система готова! Открой YouTube и покажи жест 'ОК' 👌")

while True:
    success, img = cap.get_frame()
    if not success or img is None:
        continue
    
    img = cv2.resize(img, (800, 600))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)               

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            h, w, c = img.shape 
            
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                x1, y1 = lm_list[4][1], lm_list[4][2] # Большой палец
                x2, y2 = lm_list[8][1], lm_list[8][2] # Указательный палец

                # Рисуем кружки
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                length = math.hypot(x2 - x1, y2 - y1)

                # --- ЛОГИКА НАЖАТИЯ ---
                if length < 30:
                    # Проверяем, прошло ли достаточно времени с прошлого клика
                    current_time = time.time()
                    if current_time - last_click_time > cooldown:
                        
                        # !!! НАЖИМАЕМ ПРОБЕЛ !!!
                        pyautogui.press('space')
                        
                        print("▶⏸ ПАУЗА / ПЛЕЙ")
                        
                        # Обновляем время последнего клика
                        last_click_time = current_time
                        
                        # Визуальный эффект (зеленый круг)
                        cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "SPACE PRESSED!", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        # Если перезарядка еще идет - рисуем желтый круг
                        cv2.circle(img, (x2, y2), 15, (0, 255, 255), cv2.FILLED)

    cv2.imshow("YouTube Controller", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()