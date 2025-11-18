import json
from pathlib import Path

METADATA_FILE = 'db_meta.json'
DATA_DIR = Path('data')

def load_metadata():
    """
    загрузка данных из json-файла
    """
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(data):
    """
    сохранение данных в json-файл
    """
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_table_data(table_name):
    """загружает данные таблицы из json-файла."""
    file_path = DATA_DIR / f"{table_name}.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """сохраняет данные таблицы в json-файл."""
    file_path = DATA_DIR / f"{table_name}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
