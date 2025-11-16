import prompt

def welcome():
    """
    функция приветствия пользователя
    """
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}! Welcome to the program!')
    
    # доступные компанды
    print('\n***')
    print('<command> exit - выйти из программы')
    print('<command> help - справочная информация')
    
    # обработка команд
    while True:
        command = prompt.string('Введите команду: ')
        
        if command == 'exit':
            print('Программа завершена. До свидания!')
            break
        elif command == 'help':
            print('<command> exit - выйти из программы')
            print('<command> help - справочная информация')
        else:
            print(f'Неизвестная команда: "{command}". Попробуйте "help" для списка команд.')
