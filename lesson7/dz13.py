import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ParserCBRF:
    def __init__(self, from_date="2023-01-01", to_date="2024-01-01"):
        self.data = {}
        self.from_date = from_date
        self.to_date = to_date
        self.soap_url = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx"
        self.output_file = "keyrate_data.json"

    def start(self):
        """
        Основной метод. Запускает процесс получения и сохранения данных.
        """
        logging.info("Запуск парсера ключевой ставки ЦБ РФ")
        xml_data = self._fetch_soap_data()
        self._parse_xml(xml_data)
        self._save_to_json()
        logging.info("Парсинг завершён, данные сохранены в JSON")

    def _fetch_soap_data(self):
        """
        Отправляет SOAP-запрос к веб-сервису ЦБ РФ и получает XML-ответ.
        """
        logging.info("Отправляем SOAP-запрос к веб-сервису ЦБ РФ")
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'http://web.cbr.ru/KeyRate'
        }

        from_date_iso = f"{self.from_date}T00:00:00"
        to_date_iso = f"{self.to_date}T00:00:00"

        body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <KeyRate xmlns="http://web.cbr.ru/">
      <fromDate>{from_date_iso}</fromDate>
      <ToDate>{to_date_iso}</ToDate>
    </KeyRate>
  </soap:Body>
</soap:Envelope>
"""

        response = requests.post(self.soap_url, data=body, headers=headers)
        if response.status_code != 200:
            logging.error(f"Ошибка при запросе: {response.status_code}")
            logging.error(f"Текст ошибки: {response.text}")
            raise Exception(f"Ошибка при запросе: {response.status_code}")
        logging.info("SOAP-запрос выполнен успешно, получены данные")
        return response.text

    def _parse_xml(self, xml_data):
        """
        Парсит XML-ответ, извлекает дату и значение ключевой ставки.
        """
        logging.info("Начинаем парсинг XML-ответа")
        root = ET.fromstring(xml_data)

        # Пространства имён
        ns = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'cbr': 'http://web.cbr.ru/',
            'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1'
        }

        # Находим diffgram
        diffgram = root.find('.//diffgr:diffgram', ns)
        if diffgram is None:
            logging.warning("diffgram не найден в XML")
            return

        # Находим таблицу KeyRate внутри diffgram
        keyrate_table = diffgram.find('.//KeyRate', {'xmlns': ''})
        if keyrate_table is None:
            logging.warning("Таблица KeyRate не найдена в diffgram")
            return

        # Ищем все строки KR
        for row in keyrate_table.findall('KR', {'xmlns': ''}):
            date_elem = row.find('DT', {'xmlns': ''})
            value_elem = row.find('Rate', {'xmlns': ''})

            if date_elem is not None and value_elem is not None:
                date = date_elem.text
                value = value_elem.text
                # Обработка даты: убираем часовой пояс
                date = datetime.fromisoformat(date.replace('T', ' ').split('+')[0]).strftime('%Y-%m-%d')
                self.data[date] = float(value)

        logging.info(f"Парсинг завершён, обработано {len(self.data)} записей")

    def _save_to_json(self):
        """
        Сохраняет данные в JSON-файл.
        """
        logging.info(f"Сохраняем данные в файл {self.output_file}")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в {self.output_file}")

    def _load_from_json(self):
        """
        Загружает данные из JSON-файла (для десериализации).
        """
        logging.info(f"Пытаемся загрузить данные из файла {self.output_file}")
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logging.info("Данные успешно загружены из JSON")
        else:
            logging.error(f"Файл {self.output_file} не найден")
            raise FileNotFoundError(f"Файл {self.output_file} не найден")
if __name__ == "__main__":
    parser = ParserCBRF(from_date="2023-01-01", to_date="2025-01-01")
    parser.start()
    print("Готово!")
    xcxcx
