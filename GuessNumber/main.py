from random import randint
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

gg = True
ot = 0
do = 0
max_steps = None
luseGame = 0
winGame = 0
attemps = 0

print(Fore.RED + 'Приветствую вас в своей игре "Угадай число"')
print(Fore.RED + "Здесь вам предстоит угадывать числа по подсказкам")
print(Fore.RED + "Всё просто, я загадываю число, а вы его пытаетесь отгадать")
input(Fore.RED + "Чтобы продолжить, нажмите Enter")
print()
print(Fore.YELLOW + "Выберите уровень сложности")
print(Fore.YELLOW + "1 Лёгкий (1 - 10, бесконечные попытки)")
print(Fore.YELLOW + "2 Полу-лёгкий (1 - 50, попыток - 6)")
print(Fore.YELLOW + "3 Средний (1 - 100, попыток - 8)")
print(Fore.YELLOW + "4 Сложный (1 - 500, попыток - 10)")
print(Fore.YELLOW + "5 УЛЬТРА ХАРДКОР (1 - 1000, попыток - 12)")
print()

# Устанавливаем диапазон и количество попыток в зависимости от уровня
dificlt = int(input(Fore.GREEN + "Выберите уровень сложности 1-5: "))
if dificlt == 1:
    ot, do = 1, 10
    max_steps = None
elif dificlt == 2:
    ot, do = 1, 50
    max_steps = 6
elif dificlt == 3:
    ot, do = 1, 100
    max_steps = 8
elif dificlt == 4:
    ot, do = 1, 500
    max_steps = 10
elif dificlt == 5:
    ot, do = 1, 1000
    max_steps = 12
else:
    print("Неверно, попробуйте снова")
    print()

while True:
    rand_numb = randint(ot, do)
    print(Fore.CYAN + "Я загадал число, попробуй угадать")
    print()

    while True:  # Вложенный цикл для попыток угадать число
        try:
            inputo = int(input(Fore.BLUE + f'Введи число от {ot} до {do}: '))
            print()
        except ValueError:
            print("Пожалуйста, введите целое число.")
            print()
            continue  # Возвращаемся к началу внутреннего цикла

        if gg:
            # Проверка на количество попыток
            if max_steps is not None and attemps >= max_steps:
                luseGame += 1
                total_games = winGame + luseGame
                lose_percentage = (luseGame / total_games) * 100 if total_games > 0 else 0
                print(Fore.RED + "Вы проиграли, у вас закончились попытки!")
                print(Fore.RED + f"Я загадал число {rand_numb}")
                print(Fore.RED + f"Число проигранных игр: {luseGame} ({lose_percentage:.2f}%)")
                print(Fore.RED + f"Общее количество сыгранных игр: {total_games}")
                input(Fore.RED + "Чтобы начать сначала, нажмите Enter")
                attemps = 0
                break

            # Проверка на угадывание числа
            if rand_numb == inputo:
                winGame += 1
                total_games = winGame + luseGame
                win_percentage = (winGame / total_games) * 100 if total_games > 0 else 0
                print(Fore.GREEN + "Поздравляю, вы угадали!")
                print(Fore.GREEN + f"Число выигранных игр: {winGame} ({win_percentage:.2f}%)")
                print(Fore.GREEN + f"Число шагов, за которые вы выиграли: {attemps + 1}")
                if attemps == 0:
                    print(Fore.GREEN + "Вам очень повезло!")
                input(Fore.YELLOW + "Чтобы продолжить, нажмите Enter")
                attemps = 0
                print()
                break  # Выходим из внутреннего цикла, если число угадано

            # Подсказки "больше" или "меньше"
            elif inputo < rand_numb:
                print()
                print(Fore.CYAN + "Моё число больше твоего.")
                attemps += 1
                print()
            else:
                print()
                print(Fore.CYAN + "Моё число меньше твоего.")
                attemps += 1
                print()
