import os
import io
import speech_recognition as sr
from google.cloud import speech

# Указываем путь к ключу
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account.json"

# Инициализация клиента
client = speech.SpeechClient()

# Захват аудио с микрофона
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Говорите...")
    recognizer.adjust_for_ambient_noise(source)  # Настройка под шумы
    audio = recognizer.listen(source)

# Конвертация аудио в байты
audio_data = io.BytesIO(audio.get_wav_data())

# Настройки распознавания
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="ru-RU",  # Язык распознавания
)

# Объект с аудиоданными
audio = speech.RecognitionAudio(content=audio_data.read())

# Отправка в Google Cloud для распознавания
response = client.recognize(config=config, audio=audio)

# Вывод результата
for result in response.results:
    print("Распознанный текст:", result.alternatives[0].transcript)
