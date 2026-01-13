import cv2

print("--- ЗАПУСК СКАНЕРА КАМЕР ---")

# Проверяем порты от 0 до 3
for index in range(5):
    print(f"Проверяю камеру под номером {index}...", end=" ")
    
    # Пробуем подключиться без лишних настроек (пусть Windows сама выберет драйвер)
    cap = cv2.VideoCapture(index)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"РАБОТАЕТ! ✅")
            print(f"Чтобы выйти, нажми 'q' в окне с видео.")
            
            while True:
                ret, frame = cap.read()
                if not ret: break
                
                cv2.imshow(f'Camera {index}', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            # Если нашли камеру - останавливаем поиск
            break
        else:
            print("Открылась, но черный экран 🌑")
            cap.release()
    else:
        print("Нет сигнала ❌")

print("--- ПОИСК ЗАВЕРШЕН ---")