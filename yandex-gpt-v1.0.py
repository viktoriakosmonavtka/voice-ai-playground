import requests
import json

def create_yandex_gpt_request(iam_token, model_uri, text, temperature=0.7, max_tokens=256, stop = None):
    """
    Создает структуру JSON запроса для YandexGPT.

    Args:
        iam_token (str): IAM-токен для авторизации.
        model_uri (str): URI модели YandexGPT.
        text (str): Текст запроса.
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
    "messages": [
      {
        "role": "user",
        "text": text
      }
    ]
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

while True:
    text = input("Введите вопрос (или 'exit' для выхода): ")
    if text.lower() == "exit":
        break

    headers, data = create_yandex_gpt_request(iam_token, model_uri, text)

    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        formatted_response = format_yandex_gpt_response(response_json)
        print(formatted_response)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
    except Exception as e:
        print(f"Произошла неопределённая ошибка: {e}")