def parse_where(where_str):
    """
    фильтрация, перевод строки ввода в словарь
    """
    where_str = where_str.strip()
    if '=' not in where_str:
        raise ValueError("Неверный формат условия: ожидается 'столбец = значение'")

    key, value = where_str.split('=', 1)
    key = key.strip()

    # удаление лищних пробелов и кавычек
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    elif value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            pass  

    return {key: value}

def parse_set(set_str):
    """
    обновление таблицы, приобразование ввода в словарь
    """
    set_dict = {}
    parts = set_str.split(',')
    for part in parts:
        key, value = part.split('=', 1)
        key = key.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                pass

        set_dict[key] = value
    return set_dict

def parse_values(values_str):
    """
    вставка значений, приобразование в список значений
    удаление скобок, отделяет значения через запятую, 
    """
    values_str = values_str.strip()
    if not (values_str.startswith('(') and values_str.endswith(')')):
        raise ValueError("Значения должны быть в скобках: (..., ..., ...)")
    
    values_str = values_str[1:-1].strip()
    if not values_str:
        return []
    
    # Разбиваем по запятым, но учитываем кавычки
    import shlex
    lexer = shlex.shlex(values_str, posix=True)
    lexer.whitespace = ','
    lexer.whitespace_split = True
    return [token.strip() for token in lexer]
