import os
import requests
from datetime import datetime

# Константы
DOWNLOAD_URL = "https://data.gov.ru/portal-back/api/v1/storage?id=75e8fb21-9259-4a69-8163-11c0bc0ba1cd"
DATA_DIR = "data"

def download_file(url: str, directory: str) -> str:
    """
    Скачивает файл по URL и сохраняет его в указанную директорию.
    Возвращает полный путь к скачанному файлу.
    """
    # Создаем папку, если она не существует
    os.makedirs(directory, exist_ok=True)

    # Генерируем имя файла на основе текущей даты и времени
    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    filename = f"data-{timestamp}.csv"
    filepath = os.path.join(directory, filename)

    try:
        print(f"Начинаем загрузку файла по адресу: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Проверяем на ошибки HTTP

        # Записываем содержимое в файл
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Файл успешно скачан и сохранен как: {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
        return ""

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return ""

if __name__ == "__main__":
    downloaded_file = download_file(DOWNLOAD_URL, DATA_DIR)
    if downloaded_file:
        print(f"Скачивание завершено. Файл доступен по пути: {downloaded_file}")
    else:
        print("Не удалось скачать файл.")