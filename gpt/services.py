import requests
from django.conf import settings


def ask_yandex_gpt(question):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {settings.YANDEXGPT_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{settings.YANDEXGPT_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "maxTokens": 500,
            "temperature": 0.7
        },
        "messages": [
            {"role": "user", "text": question}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['result']['alternatives'][0]['message']['text']
    else:
        return f"Ошибка: {response.status_code}"