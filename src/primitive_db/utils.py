import json
from pathlib import Path
import os

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
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_table_data(table_name, data_dir='data'):
    """
    загрузка данных таблицы из json
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f'{table_name}.json')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data, data_dir='data'):
    """
    сохранение данных таблицы в json
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f'{table_name}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
