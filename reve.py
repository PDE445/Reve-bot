import requests
import json
import base64
import os
import uuid

REVE_API_KEY = "papi.d1601689-4136-43ca-9796-3c7529fc3f7b._zEAht5URSM7_QkWiFwCmr5WkqWdL6Fp"

headers = {
    "Authorization": f"Bearer {REVE_API_KEY}", 
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def generate_reve_image(
    prompt,
    aspect_ratio="16:9",
    version="latest",
    save_json="reve_output.json",
    save_image=True
):
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "version": version
    }

    try:
        response = requests.post(
            "https://api.reve.com/v1/image/create",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        result = response.json()

        # Сохраняем JSON если нужно
        if save_json:
            with open(save_json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

        # Проверяем есть ли изображение
        if not result.get("image"):
            print("No image in response")
            return None

        # Декодируем base64
        image_data = base64.b64decode(result["image"])

        # Создаём папку images если её нет
        os.makedirs("images", exist_ok=True)

        # Уникальное имя файла
        file_name = f"{uuid.uuid4().hex}.png"
        file_path = os.path.join("images", file_name)

        # Сохраняем файл
        with open(file_path, "wb") as img_file:
            img_file.write(image_data)

        print(f"Image saved to {file_path}")

        return file_path  # <<< ВАЖНО: возвращаем путь к файлу

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
