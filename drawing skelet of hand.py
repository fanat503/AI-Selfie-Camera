import cv2
import mediapipe as mp
import time
import threading

# Using multithreading
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

# 2. Settings
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection(0.75)

address = "http://192.168.100.7:8080/video"

try:
    cap = ThreadedCamera(address)
except:
    print("Ошибка подключения! Проверь IP.")
    exit()

pTime = 0

print("Запуск! Режим: Блюр лица + Сигнализация рук")

while True:
    success, img = cap.get_frame()
    if not success or img is None:
        continue

    img = cv2.resize(img, (800, 600))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    finger_x = 0
    finger_y = 0
    hand_found = False

    results_hands = hands.process(img_rgb)

    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            
            # 1. Drawing the skeleton
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 2. Calculating the coordinates of the finger
            h, w, c = img.shape
            # We take the index finger
            lm = hand_landmarks.landmark[8]
            finger_x, finger_y = int(lm.x * w), int(lm.y * h)
            hand_found = True

            # Draw a circle on your finger
            cv2.circle(img, (finger_x, finger_y), 10, (0, 255, 0), cv2.FILLED)

    # ЭТАП 2. Looking for faces, blurring and checking
    results_face = faceDetection.process(img_rgb)

    if results_face.detections:
        for id, detection in enumerate(results_face.detections):
            
            # 1. calculating the coordinates of the face
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            
            # Coordinates
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                         int(bboxC.width * iw), int(bboxC.height * ih)
            
            # 2. Blur
            try:
                face_img = img[y:y+h, x:x+w]
                face_img = cv2.GaussianBlur(face_img, (99, 99), 30)
                img[y:y+h, x:x+w] = face_img
            except:
                pass

            # 3. ALARM
            if hand_found:
                if (finger_x > x) and (finger_x < x + w):
                    if (finger_y > y) and (finger_y < y + h):
                        
                        cv2.putText(img, "ALARM! DONT TOUCH!", (50, 100), 
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                        # Draw a red border around the face
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 4)
                    else:
                        # If we don't touch it, the frame is purple.
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
            else:
                # If there is no hand, just a frame.
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)

    # Stage 3. FPS 
    cTime = time.time()
    fps = 1 / (cTime - pTime) 
    pTime = cTime  

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 255, 0), 2)

    cv2.imshow("Frankenstein: Anonymous + Alarm", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()