import cv2
import mediapipe as mp
import threading

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

cap = ThreadedCamera("http://192.168.100.7:8080/video")
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Launching the neural network
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    success, img = cap.read()
    
    # Checking
    if not success:
        print("Жду камеру...")
        continue

    
    img = cv2.resize(img, (800, 600))

    # Конвертируем цвета
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 2. Looking for hands
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('Selfie Camera', img)

    # Exit by clicking
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()