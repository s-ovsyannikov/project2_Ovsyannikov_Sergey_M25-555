from .parser import parse_set, parse_values, parse_where
from .utils import load_table_data, save_table_data

SUPPORTED_TYPES = {'int': int, 'str': str, 'bool': bool}

def insert(metadata, table_name, values_str):
    """добавление данных в таблицу"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    # парсинг ввода
    try:
        values = parse_values(values_str)
    except ValueError as e:
        print(f'Некорректное значение: {values_str}. {e}')
        return None

    # схема таблицы
    columns = metadata[table_name]  
    expected_count = len(columns) - 1 
    if len(values) != expected_count:
        print(f'Ошибка: Ожидалось {expected_count} значений (без ID), получено {len(values)}.')
        return None

    
    table_data = load_table_data(table_name)

    # генерация ID
    new_id = 1 if not table_data else max(row['ID'] for row in table_data) + 1

    # создание записи
    record = {'ID': new_id}
    for i, col in enumerate(columns[1:]):  
        col_name, col_type_str = col.split(':')
        col_type = SUPPORTED_TYPES[col_type_str]

        # проверка типов
        val = values[i]
        if col_type is int:
            try:
                val = int(val)
            except ValueError:
                print(f'Ошибка: Значение "{val}" не является целым числом для столбца "{col_name}".')
                return None
        elif col_type is bool:
            if val.lower() == 'true':
                val = True
            elif val.lower() == 'false':
                val = False
            else:
                print(f'Ошибка: Значение "{val}" не является bool для столбца "{col_name}".')
                return None
        

        record[col_name] = val

    # добавление записи
    table_data.append(record)
    save_table_data(table_name, table_data)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data

def select(table_data, where_clause=None):
    """извлечение данных из табилцы"""
    if not where_clause:
        return table_data

    result = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break
        if match:
            result.append(row)
    return result

def update(metadata, table_name, set_str, where_str):
    """обновление записи по заданному условию"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    try:
        set_clause = parse_set(set_str)
    except ValueError as e:
        print(f'Ошибка в set-условии: {e}')
        return None

    try:
        where_clause = parse_where(where_str)
    except ValueError as e:
        print(f'Ошибка в where-условии: {e}')
        return None

    table_data = load_table_data(table_name)
    updated = False

    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break

        if match:
            for k, v in set_clause.items():
                if k in row:
                    row[k] = v
                    updated = True

    if updated:
        save_table_data(table_name, table_data)
        print(f'Записи в таблице "{table_name}" успешно обновлены.')
    else:
        print('Нет записей, соответствующих условию where.')

    return table_data if updated else None

def delete(metadata, table_name, where_str):
    """удаление записи по заданному условию"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    try:
        where_clause = parse_where(where_str)
    except ValueError as e:
        print(f'Ошибка в where-условии: {e}')
        return None

    table_data = load_table_data(table_name)
    filtered_data = []

    deleted_count = 0
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break
        if not match:
            filtered_data.append(row)
        else:
            deleted_count += 1

    if deleted_count > 0:
        save_table_data(table_name, filtered_data)
        print(f'Удалено {deleted_count} записей из таблицы "{table_name}".')
        return filtered_data
    else:
        print('Нет записей, соответствующих условию where.')
        return None

def info(metadata, table_name):
    """информация о таблице"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name]
    table_data = load_table_data(table_name)

    print(f'Таблица: {table_name}')
    print(f'Столбцы: {", ".join(columns)}')
    print(f'Количество записей: {len(table_data)}')

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

    #сохранение метаданных
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
