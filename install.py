import sys
import subprocess

print(f"Лечим ошибку 'no attribute solutions' в: {sys.executable}")

# 1. Удаляем "плохой" protobuf
print("Удаляю новую версию protobuf...")
subprocess.call([sys.executable, '-m', 'pip', 'uninstall', 'protobuf', '-y'])

# 2. Ставим "правильный" protobuf (старой версии)
print("Устанавливаю правильную версию...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', "protobuf<4.0.0"])

# 3. На всякий случай обновляем mediapipe
print("Проверяю mediapipe...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', "mediapipe"])

print("\n--- ЛЕЧЕНИЕ ЗАВЕРШЕНО! ---")
print("Теперь запускай основной код. Должно работать!")