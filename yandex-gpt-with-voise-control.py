import requests
import json
import speech_recognition as sr
import pyttsx3
import time

# ... (Функции create_yandex_gpt_request и format_yandex_gpt_response) ...

def create_yandex_gpt_request(iam_token, model_uri, messages, temperature=0.7, max_tokens=256, stop = None):
    """
    Создает структуру JSON запроса для YandexGPT.

    Args:
        iam_token (str): IAM-токен для авторизации.
        model_uri (str): URI модели YandexGPT.
        messages (list): Список сообщений в формате [{"role": "user/assistant", "text": text}]
        temperature (float): Температура для случайности генерации (0 - 1).
        max_tokens (int): Максимальное количество токенов для генерации.
        stop (list): Список стоп-слов

    Returns:
        dict: Структура запроса в формате JSON.
    """
    headers = {
    "Authorization": f"Bearer {iam_token}",
    "Content-Type": "application/json"
    }
    data = {
    "modelUri": model_uri,
    "completionOptions": {
      "stream": False,
      "temperature": temperature,
      "maxTokens": max_tokens,
      "stop": stop
    },
    "messages": messages
  }
    return headers, json.dumps(data)

def format_yandex_gpt_response(response_json):
    """
    Преобразует JSON-ответ от YandexGPT в красивый текстовый вывод.

    Args:
        response_json (dict): JSON-ответ от YandexGPT.

    Returns:
        str: Строка с форматированным ответом.
    """
    if not isinstance(response_json, dict):
        return "Ошибка: Неверный формат ответа."

    try:
        alternatives = response_json.get("result", {}).get("alternatives", [])
        if not alternatives:
            return "Нет доступных вариантов ответа."

        formatted_text = ""
        for i, alternative in enumerate(alternatives):
          message = alternative.get("message", {})
          text = message.get("text", "Нет текста")
          formatted_text += f"Ответ #{i+1}:\n{text}\n\n"

        usage = response_json.get("result", {}).get("usage", {})
        formatted_text += f"Использовано токенов:\n"
        formatted_text += f"  Входных: {usage.get('inputTextTokens', 'нет информации')}\n"
        formatted_text += f"  Выходных: {usage.get('completionTokens', 'нет информации')}\n"
        formatted_text += f"  Всего: {usage.get('totalTokens', 'нет информации')}\n"

        formatted_text += f"\nМодель: {response_json.get('result', {}).get('modelVersion', 'нет информации')}"

        return formatted_text

    except Exception as e:
        return f"Ошибка форматирования: {e}"


iam_token = ""
model_uri = "gpt://b1ggu3hn2621to3uvfiq/yandexgpt-lite"
api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

fixed_context = [
    {"role": "user", "text": "Ты ассистент, созданный компанией Yandex."},
    {"role": "assistant", "text": "Я готов помогать."},
    {"role": "user", "text": "Ты должен всегда отвечать вежливо и по делу."},
    {"role": "assistant", "text": "Хорошо, я постараюсь."},
    {"role": "user", "text": "Твоя основная задача - отвечать на вопросы."},
]
chat_history = []
MAX_HISTORY_LENGTH = 10

recognizer = sr.Recognizer()
engine = pyttsx3.init()

while True:
    ready = input("Готовы ли вы задать вопрос? (да/нет): ").lower()

    if ready == "да":
        with sr.Microphone() as source:
            print("Говорите вопрос...")
            audio = recognizer.listen(source)

        try:
            question = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {question}")

            chat_history.append({"role": "user", "text": question})

            # Ограничение размера истории
            if len(chat_history) > MAX_HISTORY_LENGTH:
                chat_history = chat_history[-MAX_HISTORY_LENGTH:]

            # Объединение контекстов
            messages_to_send = fixed_context + chat_history

            headers, data = create_yandex_gpt_request(iam_token, model_uri, messages_to_send)

            response = requests.post(api_url, headers=headers, data=data)
            response.raise_for_status()
            response_json = response.json()
            answer = response_json.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "Нет ответа")

            chat_history.append({"role": "assistant", "text": answer})
            formatted_response = format_yandex_gpt_response(response_json)
            print(formatted_response)

            time.sleep(7)

            engine.say(answer)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Не удалось распознать голос.")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
        except Exception as e:
            print(f"Произошла неопределённая ошибка: {e}")
    elif ready == "нет":
        print("Окей, когда будете готовы, введите 'да'.")
    else:
        print("Пожалуйста, введите 'да' или 'нет'.")