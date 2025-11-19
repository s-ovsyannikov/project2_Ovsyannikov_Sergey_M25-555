import time
from functools import wraps


def handle_db_errors(func):
    """
    обработка ошибок
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f'Ошибка: Обращение к несуществующему объекту - {e}')
            return None
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
            return None
        except FileNotFoundError as e:
            print(f'Ошибка файла: {e}')
            return None
        except Exception as e:
            print(f'Неожиданная ошибка в функции {func.__name__}: {e}')
            return None
    return wrapper

def confirm_action(action_name):
    """
    подтверждение операций
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get('confirm') is False:
                return func(*args, **kwargs)
                
            user_input = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            if user_input == 'y':
                return func(*args, **kwargs)
            else:
                print('Операция отменена.')
                return None
        return wrapper
    return decorator

def log_time(func):
    """
    счетчик времени
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f'Функция {func.__name__} выполнилась за {execution_time:.3f} секунд')
        return result
    return wrapper

def create_cacher():
    """
    кэшер с замыканием
    """
    cache = {}
    
    def cache_result(key, value_func):
        """
        кэширование результата функции
        """
        if key in cache:
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            return result
    
    def clear_cache():
        """
        очистка кэша
        """
        cache.clear()
        print("Кэш очищен")
    
    
    cache_result.clear = clear_cache
    
    return cache_result
