import pyttsx3

# 1. Инициализация движка (создаем робота)
engine = pyttsx3.init()

# 2. Настройка голоса (необязательно, но круто)
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id) # Обычно 0 - мужской, 1 - женский (зависит от винды)

# 3. Настройка скорости
engine.setProperty('rate', 200) # 150 - нормально, 200 - быстро

# 4. Действие
text = "Привет! Я твой новый ассистент."
print(f"Говорю: {text}")

engine.say(text) # Добавить фразу в очередь
engine.runAndWait() # Сказать всё, что в очереди