import requests
import base64
import os
import uuid


class LeonardoService:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1/generations"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt: str) -> str | None:
        payload = {"prompt": prompt, "num_images": 1, "width": 1024, "height": 1024}

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )

            # ✅ Тут response уже есть
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

            response.raise_for_status()
            result = response.json()

            generation_id = result.get("sdGenerationJob", {}).get("generationId")
            if not generation_id:
                print("No generationId found")
                return None

            return self._download_image(generation_id)

        except Exception as e:
            print("Leonardo error:", e)
            return None


    def _download_image(self, generation_id: str) -> str | None:
        """
        Получает готовое изображение по generation_id
        """
        resp = requests.get(f"{self.base_url}/{generation_id}", headers=self.headers)

        try:
            response = requests.get(
                f"{self.base_url}/{generation_id}",
                headers=self.headers
            )

            response.raise_for_status()
            result = response.json()

            images = result.get("generations_by_pk", {}).get("generated_images")

            if not images:
                print("No images found")
                return None

            image_url = images[0].get("url")

            image_response = requests.get(image_url)
            image_response.raise_for_status()

            return self._save_image(image_response.content)

        except Exception as e:
            print("Download error:", e)
            return None
        print("DOWNLOAD STATUS:", resp.status_code)
        print("DOWNLOAD RESPONSE:", resp.text)

    def _save_image(self, image_bytes: bytes) -> str:
        """
        Сохраняет изображение и возвращает путь.
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "..", "images")
        os.makedirs(images_dir, exist_ok=True)

        file_name = f"{uuid.uuid4().hex}.png"
        file_path = os.path.join(images_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return file_path
        