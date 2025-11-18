from prettytable import PrettyTable

from .utils import load_table_data, save_table_data

SUPPORTED_TYPES = {'int', 'str', 'bool'}

def create_table(metadata, table_name, columns):
    """
    создание таблицы
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    parsed_columns = []
    for col in columns:
        if ':' not in col:
            print(f'Некорректное значение: {col}. Формат: имя:тип')
            return None
        name, dtype = col.split(':', 1)
        if not name or dtype not in SUPPORTED_TYPES:
            print(f'Некорректное значение: {col}. Тип должен быть int, str или bool.')
            return None
        parsed_columns.append(f'{name}:{dtype}')

    final_columns = ['ID:int'] + parsed_columns

    # сохранение метаданных
    metadata[table_name] = final_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(final_columns)}')
    return metadata

def drop_table(metadata, table_name):
    """
    удаление таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """
    список всех таблиц
    """
    if not metadata:
        print('Нет созданных таблиц.')
        return

    for table in sorted(metadata.keys()):
        print(f'- {table}')

def _parse_value(value_str, expected_type):
    """
    парсинг значения согласно ожидаемому типу
    """
    value_str = value_str.strip()
    
    if expected_type == 'int':
        try:
            return int(value_str)
        except ValueError:
            raise ValueError(f'Некорректное целое число: {value_str}')
    
    elif expected_type == 'bool':
        if value_str.lower() in ('true', '1', 'yes'):
            return True
        elif value_str.lower() in ('false', '0', 'no'):
            return False
        else:
            raise ValueError(f'Некорректное булево значение: {value_str}')
    
    elif expected_type == 'str':
        # Убираем кавычки если они есть
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        return value_str
    
    return value_str

def _convert_to_string(value):
    """
    конвертация значения в строку для вывода
    """
    if isinstance(value, bool):
        return str(value)
    return value

def insert(metadata, table_name, values):
    """
    вставка данных в таблицу
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    # Загружаем текущие данные
    table_data = load_table_data(table_name)
    
    # Получаем схему таблицы (без ID)
    columns_schema = metadata[table_name]
    data_columns = columns_schema[1:]  # исключаем ID
    
    # Проверяем количество значений
    if len(values) != len(data_columns):
        print(f'Ошибка: Ожидается {len(data_columns)} значений, получено {len(values)}')
        return None
    
    # Парсим значения согласно типам
    parsed_values = []
    for i, value in enumerate(values):
        col_name, col_type = data_columns[i].split(':')
        try:
            parsed_value = _parse_value(value, col_type)
            parsed_values.append(parsed_value)
        except ValueError as e:
            print(f'Ошибка в значении "{value}" для столбца "{col_name}": {e}')
            return None
    
    # Генерируем ID
    new_id = 1
    if table_data:
        ids = [record['ID'] for record in table_data]
        new_id = max(ids) + 1
    
    # Создаем запись
    record = {'ID': new_id}
    for i, col in enumerate(data_columns):
        col_name = col.split(':')[0]
        record[col_name] = parsed_values[i]
    
    # Добавляем запись
    table_data.append(record)
    save_table_data(table_name, table_data)
    
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data

def _parse_where_clause(where_str):
    """
    парсинг условия WHERE (более гибкий)
    """
    # Поддерживаем разные форматы: "age = 19", "age=19", "name = 'Natalia'"
    if '=' in where_str:
        parts = where_str.split('=', 1)
        column = parts[0].strip()
        value = parts[1].strip()
        return {'column': column, 'value': value}
    
    return None

def _parse_set_clause(set_str):
    """
    парсинг условия SET (более гибкий)
    """
    if '=' in set_str:
        parts = set_str.split('=', 1)
        column = parts[0].strip()
        value = parts[1].strip()
        return {'column': column, 'value': value}
    
    return None

def select(metadata, table_name, where_clause=None):
    """
    выборка данных из таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    
    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return
    
    # Фильтруем данные если есть условие
    filtered_data = table_data
    if where_clause:
        where_parsed = _parse_where_clause(where_clause)
        if not where_parsed:
            print('Некорректное условие WHERE.')
            return
        
        column = where_parsed['column']
        value = where_parsed['value']
        
        # Определяем тип столбца для парсинга значения
        col_type = 'str'  # по умолчанию
        for col_schema in metadata[table_name]:
            col_name, col_type_str = col_schema.split(':')
            if col_name == column:
                col_type = col_type_str
                break
        
        try:
            parsed_value = _parse_value(value, col_type)
        except ValueError as e:
            print(f'Ошибка в условии WHERE: {e}')
            return
        
        filtered_data = [record for record in table_data 
                        if str(record.get(column, '')) == str(parsed_value)]
    
    if not filtered_data:
        print('Записи не найдены.')
        return
    
    # Создаем красивую таблицу для вывода
    table = PrettyTable()
    table.field_names = [col.split(':')[0] for col in metadata[table_name]]
    
    for record in filtered_data:
        row = []
        for col in metadata[table_name]:
            col_name = col.split(':')[0]
            row.append(_convert_to_string(record.get(col_name, '')))
        table.add_row(row)
    
    print(table)

def update(metadata, table_name, set_clause, where_clause):
    """
    обновление данных в таблице
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    table_data = load_table_data(table_name)
    
    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return None
    
    # Парсим условия
    set_parsed = _parse_set_clause(set_clause)
    where_parsed = _parse_where_clause(where_clause)
    
    if not set_parsed or not where_parsed:
        print('Некорректный формат SET или WHERE условия.')
        return None
    
    # Определяем тип для SET значения
    set_col_type = 'str'
    for col_schema in metadata[table_name]:
        col_name, col_type_str = col_schema.split(':')
        if col_name == set_parsed['column']:
            set_col_type = col_type_str
            break
    
    # Определяем тип для WHERE значения
    where_col_type = 'str'
    for col_schema in metadata[table_name]:
        col_name, col_type_str = col_schema.split(':')
        if col_name == where_parsed['column']:
            where_col_type = col_type_str
            break
    
    try:
        set_value = _parse_value(set_parsed['value'], set_col_type)
        where_value = _parse_value(where_parsed['value'], where_col_type)
    except ValueError as e:
        print(f'Ошибка в значении: {e}')
        return None
    
    # Находим и обновляем записи
    updated_count = 0
    updated_ids = []
    
    for record in table_data:
        if str(record.get(where_parsed['column'], '')) == str(where_value):
            record[set_parsed['column']] = set_value
            updated_count += 1
            updated_ids.append(record['ID'])
    
    if updated_count == 0:
        print('Записи для обновления не найдены.')
        return None
    
    save_table_data(table_name, table_data)
    print(f'Запись с ID={updated_ids[0]} в таблице "{table_name}" успешно обновлена.')
    return table_data

def delete(metadata, table_name, where_clause):
    """
    удаление данных из таблицы
    """
    print(f"DEBUG: table_name={table_name}, where_clause='{where_clause}'")
    
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    table_data = load_table_data(table_name)
    
    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return None
    
    where_parsed = _parse_where_clause(where_clause)
    if not where_parsed:
        print('Некорректное условие WHERE.')
        return None
    
    # Определяем тип для WHERE значения
    where_col_type = 'str'
    for col_schema in metadata[table_name]:
        col_name, col_type_str = col_schema.split(':')
        if col_name == where_parsed['column']:
            where_col_type = col_type_str
            break
    
    try:
        where_value = _parse_value(where_parsed['value'], where_col_type)
    except ValueError as e:
        print(f'Ошибка в условии WHERE: {e}')
        return None
    
    # Находим записи для удаления
    records_to_keep = []
    deleted_ids = []
    
    for record in table_data:
        if str(record.get(where_parsed['column'], '')) == str(where_value):
            deleted_ids.append(record['ID'])
        else:
            records_to_keep.append(record)
    
    if not deleted_ids:
        print('Записи для удаления не найдены.')
        return None
    
    save_table_data(table_name, records_to_keep)
    print(f'Запись с ID={deleted_ids[0]} успешно удалена из таблицы "{table_name}".')
    return records_to_keep

def info(metadata, table_name):
    """
    информация о таблице
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    
    print(f'Таблица: {table_name}')
    print(f'Столбцы: {", ".join(metadata[table_name])}')
    print(f'Количество записей: {len(table_data)}')