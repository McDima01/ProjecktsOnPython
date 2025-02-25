"""2. Игра "Камень, ножницы, бумага"
Простая игра против компьютера. Компьютер выбирает случайный ход, а пользователь вводит свой. Программа определяет победителя.
"""
from random import randint
from time import sleep
import os
import sys
import colorama
from colorama import Fore
from colorama import init, Fore
init(strip=False, autoreset=True)
print(Fore.GREEN + "Приветствую!")
colorama.init(autoreset=True)

# Включение цветовой поддержки в Windows
if sys.platform.startswith('win'):
    os.system('')

win = 0
lose = 0
move = None
run = None
last_numbers = []  # Список для отслеживания последних чисел


print(Fore.GREEN + "              Приветствую!")
print(Fore.GREEN + "Вы попали в игру \"Камень ножницы бумага\"")
print(Fore.GREEN + "Знаете ли вы правила?")
jshd = str(input(Fore.GREEN + 'Напишите да/нет: '))
if jshd == "нет" or jshd == "Нет":
    print(Fore.YELLOW + "          Правила:")
    print(Fore.YELLOW + "1. Камень бьёт ножницы")
    print(Fore.YELLOW + "2. Ножницы режут бумагу")
    print(Fore.YELLOW + "3. Бумага покрывает камень")
    print(Fore.YELLOW + "4. В других случаях вы проиграете")
    print("")
else:
    print(Fore.YELLOW + "Тогда продолжим: ")
    print()

while True:
    rand_numb = randint(1, 3)

    # Проверяем, если число повторяется более двух раз подряд
    if last_numbers.count(rand_numb) < 2:
        last_numbers.append(rand_numb)

        # Сохраняем только последние два числа
        if len(last_numbers) > 2:
            last_numbers.pop(0)
    while True:
        while run:
            print(Fore.LIGHTGREEN_EX + '     Ваша статистика:')
            print(Fore.LIGHTGREEN_EX + F"Вы выйграли {win} раз")
            print(Fore.LIGHTGREEN_EX + f'Вы проиграли {lose} раз')
            print()
            break


        user_input = input(Fore.BLUE + "Введите жест который хотите показать: ") #получение жеста от пользователя
        if user_input not in ["камень", "ножницы", "бумага"]:
             print(Fore.RED + "Вы ввели не правильное действие, попробуйте ещё раз!")
             print()
        else:
            run = True
            break

    if rand_numb == 1: #придание числу значения
        move = 'камень'
    elif rand_numb == 2:
        move = "ножницы"
    else:
        move = "бумага"

    while True:
        # цикл для проверки, выиграл ли пользователь
        if user_input == move and user_input in ["камень", "ножницы", "бумага"]:
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            sleep(1)
            print()
            print(Fore.YELLOW + f"Я сыграл: \"{move}\" ")
            sleep(1)
            print()
            print(Fore.CYAN + "У нас ничья")
            print()
            sleep(1)
            print(Fore.GREEN + "Начинаем новый раунд")
            print()
            sleep(2)
            move = None
            break
        elif user_input == "ножницы" and move == "камень":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.CYAN + "К сожаленью камень бьёт ножницы")
            print(Fore.GREEN + "Я выйграл!")
            print()
            sleep(2)
            lose += 1
            move = None
            break
        elif user_input == "ножницы" and move == "бумага":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.GREEN + "К счастью ножницы режут бумагу")
            print(Fore.GREEN + "Ты выйграл!")
            print()
            sleep(2)
            win += 1
            move = None
            break
        elif user_input == "бумага" and move == "камень":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.RED + "К сожаленью бумага покрывает камень")
            print(Fore.GREEN + "Я проиграл:(")
            print()
            sleep(2)
            win += 1
            move = None
            break
        elif user_input == "бумага" and move == "ножницы":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.RED + "К счастью ножницы режут бумагу")
            print(Fore.RED + "Ты проиграл:(")
            print()
            sleep(2)
            lose += 1
            move = None
            break
        elif user_input == "камень" and move == "ножницы":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.GREEN + "К счастью камень бьёт ножницы")
            print(Fore.GREEN + "Ты выйграл!")
            print()
            sleep(2)
            win += 1
            move = None
            break
        elif user_input == "камень" and move == "бумага":
            print(Fore.GREEN + f'Вы ввели: "{user_input}"')
            print()
            sleep(1)
            print(Fore.YELLOW + f'Я сыграл: "{move}"')
            print()
            sleep(1)
            print(Fore.RED + "К сожаленью бумага накрывает камень")
            print(Fore.RED + "Я выйграл!")
            print()
            sleep(2)
            lose += 1
            move = None
            break

