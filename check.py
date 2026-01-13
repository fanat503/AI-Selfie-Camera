import sys
import mediapipe

print("--- ИНФОРМАЦИЯ О СИСТЕМЕ ---")
print(f"Версия Python: {sys.version}")
print(f"Откуда берется mediapipe: {mediapipe.__file__}")

try:
    print("Есть ли solutions внутри?", 'solutions' in dir(mediapipe))
except:
    print("Не удалось проверить содержимое.")
    