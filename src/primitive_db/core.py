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
