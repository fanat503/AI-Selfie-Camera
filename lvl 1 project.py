import cv2

# Твой адрес
cap = cv2.VideoCapture("http://192.168.100.7:8080/video")

while True:
    success, img = cap.read()
    
    # ПРОВЕРКА
    if not success:
        print("Жду камеру...")
        continue

    
    img = cv2.resize(img, (800, 600))

    
    cv2.imshow('Selfie Camera', img)

    # команда выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()