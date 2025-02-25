from random import randint, choice
from time import sleep
import colorama
colorama.init(autoreset=True)
import os
import sys
import colorama
from colorama import Fore
from colorama import init, Fore

init(strip=False, autoreset=True)

# Включение цветовой поддержки в Windows
if sys.platform.startswith('win'):
    os.system('')

# Инициализация
win, lose = 0, 0
gestures = ["камень", "ножницы", "бумага"]
rules = {
    "камень": {"ножницы": "Камень бьёт ножницы", "бумага": "Бумага покрывает камень"},
    "ножницы": {"бумага": "Ножницы режут бумагу", "камень": "Камень бьёт ножницы"},
    "бумага": {"камень": "Бумага покрывает камень", "ножницы": "Ножницы режут бумагу"},
}
last_computer_choices = []  # Список для отслеживания последних выборов компьютера


def print_rules():
    print(Fore.YELLOW + "          Правила:")
    print(Fore.YELLOW + "1. Камень бьёт ножницы")
    print(Fore.YELLOW + "2. Ножницы режут бумагу")
    print(Fore.YELLOW + "3. Бумага покрывает камень")
    print(Fore.YELLOW + "4. В других случаях вы проигруете")
    print()


def show_stats():
    print(Fore.LIGHTGREEN_EX + "     Ваша статистика:")
    print(Fore.LIGHTGREEN_EX + f"Вы выиграли {win} раз")
    print(Fore.LIGHTGREEN_EX + f"Вы проиграли {lose} раз")
    print()


def get_computer_choice():
    """Выбирает жест для компьютера, избегая частых повторений."""
    while True:
        choice_ = choice(gestures)
        if last_computer_choices.count(choice_) < 2:  # Не более двух повторений
            last_computer_choices.append(choice_)
            if len(last_computer_choices) > 3:  # Храним только последние 3 выбора
                last_computer_choices.pop(0)
            return choice_


# Приветствие
print(Fore.GREEN + "              Приветствую!")
print(Fore.GREEN + 'Вы попали в игру "Камень, ножницы, бумага"')
print(Fore.GREEN + "Знаете ли вы правила?")
jshd = input(Fore.GREEN + 'Напишите да/нет: ').strip().lower()
if jshd in ["нет", "н"]:
    print_rules()

# Основной игровой цикл
while True:
    computer_choice = get_computer_choice()  # Компьютер выбирает жест
    user_input = input(Fore.BLUE + "Введите жест (камень, ножницы, бумага): ").strip().lower()

    if user_input not in gestures:
        print(Fore.RED + "Вы ввели неверное действие, попробуйте снова!")
        continue

    # Отображение выборов
    print(Fore.GREEN + f'Вы выбрали: "{user_input}"')
    print()
    sleep(1)
    print(Fore.YELLOW + f'Компьютер выбрал: "{computer_choice}"')
    print()
    sleep(1)

    # Определение результата
    if user_input == computer_choice:
        print(Fore.CYAN + "Ничья! Начинаем новый раунд.")
        print()
    elif computer_choice in rules[user_input]:
        print(Fore.GREEN + rules[user_input][computer_choice])
        print(Fore.GREEN + "Вы выиграли!")
        print()
        win += 1
    else:
        print(Fore.RED + rules[computer_choice][user_input])
        print(Fore.RED + "Вы проиграли!")
        print()
        lose += 1

    # Показ статистики
    sleep(1)
    show_stats()
    print(Fore.GREEN + "Начинаем новый раунд!")
    sleep(2)
