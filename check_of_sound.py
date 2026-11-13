import wave

def check_audio_format(filename):
    """Проверяет формат аудиофайла и выводит подробную информацию в консоль.

    Args:
        filename: Путь к аудиофайлу.
    """
    try:
        with wave.open(filename, 'rb') as wf:
            print(f"Информация об аудиофайле '{filename}':")
            print(f"  Количество каналов: {wf.getnchannels()}")
            print(f"  Частота дискретизации: {wf.getframerate()} Гц")
            print(f"  Разрядность: {wf.getsampwidth() * 8} бит")
            print(f"  Количество фреймов: {wf.getnframes()}")
            print(f"  Длительность: {wf.getnframes() / wf.getframerate():.2f} сек")
            print(f"  Компрессия: {wf.getcomptype()}")
            print(f"  Компрессионные данные: {wf.getcompname()}")

            # Проверка на соответствие требованиям Vosk
            if wf.getnchannels() != 1:
                print("  ВНИМАНИЕ: Файл не является монофоническим (не один канал). Vosk может не работать корректно.")
            if wf.getframerate() != 16000:
                print("  ВНИМАНИЕ: Частота дискретизации не равна 16000 Гц. Vosk может не работать корректно.")
            if wf.getsampwidth() != 2:
                print("  ВНИМАНИЕ: Разрядность не равна 16 бит. Vosk может не работать корректно.")

    except wave.Error as e:
        print(f"Ошибка при открытии файла: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")

# Пример использования:
check_audio_format("decoder-test.wav")