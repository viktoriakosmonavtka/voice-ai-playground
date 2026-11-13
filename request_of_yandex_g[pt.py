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


iam_token = ""
# Пример использования с моделью yandexgpt-lite:
model_uri = "gpt://b1ggu3hn2621to3uvfiq/yandexgpt-lite"  # Используем yandexgpt-lite
text = "Привет, как дела?"
headers, data = create_yandex_gpt_request(iam_token, model_uri, text)

#Теперь нужно отправить запрос
try:
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers, data=data)
    response.raise_for_status() #проверяем код ответа, если не 200 то raise error
    response_json = response.json()
    print(response_json) # выводим ответ
except requests.exceptions.RequestException as e:
    print(f"Ошибка при отправке запроса: {e}")
except json.JSONDecodeError as e:
    print(f"Ошибка декодирования JSON: {e}")
except Exception as e:
    print(f"Произошла неопределённая ошибка: {e}")