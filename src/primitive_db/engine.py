import shlex

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata

METADATA_FILE = 'db_meta.json'

def print_help():
    """справочная информация"""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """основной рабочий цикл."""
    while True:
        metadata = load_metadata(METADATA_FILE)

        try:
            user_input = input('>>> Введите команду: ').strip()
            if not user_input:
                continue

            args = shlex.split(user_input)
            command = args[0].lower()

            if command == 'create_table':
                if len(args) < 3:
                    print('Недостаточно аргументов. Формат: create_table <имя> <столбец:тип> ...')
                    continue
                table_name = args[1]
                columns = args[2:]
                result = create_table(metadata, table_name, columns)
                if result is not None:
                    save_metadata(METADATA_FILE, result)

            elif command == 'drop_table':
                if len(args) != 2:
                    print('Неверный формат. Используйте: drop_table <имя_таблицы>')
                    continue
                table_name = args[1]
                result = drop_table(metadata, table_name)
                if result is not None:
                    save_metadata(METADATA_FILE, result)

            elif command == 'list_tables':
                list_tables(metadata)

            elif command == 'help':
                print_help()

            elif command == 'exit':
                print('Программа завершена. До свидания!')
                break

            else:
                print(f'Функции "{command}" нет. Попробуйте снова.')

        except KeyboardInterrupt:
            print('\nПрограмма прервана пользователем. До свидания!')
            break
        except Exception as e:
            print(f'Неожиданная ошибка: {e}. Попробуйте снова.')
