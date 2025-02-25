from asteval import Interpreter
from colorama import Fore

print(Fore.YELLOW + 'Это калькулятор.\n')

while True:
    user_input = input(Fore.GREEN + 'Просто введите выражение которое хотите расщитать: ').split(" ")

    def calculate(user_input):
        move = ' '.join(user_input)  # Соединяем части в одну строку
        move = move.replace('÷', '/').replace('\\', '/')  # Заменяем '÷' и '\' на '/'
        aeval = Interpreter()  # Создаем интерпретатор
        try:
            result = aeval(move)  # Вычисляем результат
            return result
        except Exception as e:
            return f"Ошибка: {e}"


    result = calculate(user_input)
    expression = ' '.join(user_input)

    print(Fore.CYAN + f'{expression} = {result}')