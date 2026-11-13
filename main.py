import speech_recognition as sr
import sounddevice as sd
import numpy as np
import wave
import time

# Параметры записи
samplerate = 8000
channels = 1
dtype = np.int16
duration = 5 # Уменьшим длительность записи до 3 секунд.
frames = int(duration*samplerate)
filename = "recorded_speaker.wav"

def record_from_speaker(filename, duration, samplerate, channels, dtype, frames):
    """Записывает звук с динамика и сохраняет его в файл."""
    print("Запись начата...")
    try:
        myrecording = sd.rec(int(frames), samplerate=samplerate, channels=channels, dtype=dtype)
        sd.wait()  # Wait until recording is finished
    except Exception as e:
       print(f"Ошибка записи: {e}")
       return None
    print("Запись окончена")
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(dtype(0).nbytes)
        wf.setframerate(samplerate)
        wf.writeframes(myrecording.tobytes())
    return myrecording.tobytes()

def recognize_audio(audio_data, samplerate):
    """Распознает аудио с помощью SpeechRecognition и возвращает распознанный текст."""
    try:
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
          audio = r.record(source)
        try:
            return r.recognize_google(audio, language="ru-RU")
        except Exception as e:
             print(f"Ошибка распознавания {e}")
             return ""
    except Exception as e:
        print(f"Ошибка: {e}")
        return ""

if __name__ == "__main__":
    # Запись с динамика
    audio_data = record_from_speaker(filename, duration, samplerate, channels, dtype, frames)

    if audio_data is None:
        print("Не удалось записать звук")
        exit()
    # Распознавание текста
    recognized_text = recognize_audio(audio_data, samplerate)

    # Вывод результата
    if recognized_text:
        print("Распознанный текст:")
        print(recognized_text)
    else:
        print("Не удалось распознать текст.")