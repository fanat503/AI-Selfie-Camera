import sys
import subprocess

print(f"Устанавливаю библиотеки для Питона по адресу:\n{sys.executable}")

# Эта команда запускает pip install прямо из текущего питона
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'SpeechRecognition'])

# А эта библиотека нужна на Windows для голоса (иногда pyttsx3 без неё не работает)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyaudio'])

print("\n--- ГОТОВО! ---")
print("Теперь попробуй запустить свой код с голосом.")