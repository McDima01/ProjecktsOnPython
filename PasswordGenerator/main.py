"""
5. Генератор паролей
   Напишите программу, которая генерирует случайные пароли определенной длины, содержащие буквы, цифры и специальные символы.
"""
"""Некоторые функции и константы модуля string:
string.ascii_letters. Объединение констант ascii_lowercase и ascii_uppercase
string.ascii_lowercase. Строчные буквы «abcdefghijklmnopqrstuvwxyz»
string.ascii_uppercase. Заглавные буквы «ABCDEFGHIJKLMNOPQRSTUVWXYZ»
string.digits. Строка «0123456789»
string.hexdigits. Строка «0123456789abcdefABCDEF»
string.octdigits. Строка «01234567»
string.punctuation. Строка символов ASCII, 
которые считаются символами пунктуации в локали C: !"#$%&'()*+,-./:;<=>?@[]^_`{|}~
"""
import random
import string


def welcome_skript():
    print("Приветствую! Это генератор паролей")
    input("Чтобы начать нажмите enter ")
    print()

def get_random_password(lengths, letter):
    # выбор из всех строчных букв
    # letters = string.ascii_letters + string.digits + string.punctuation
    result_str = ''.join(random.choice(letter) for i in range(lengths))
    print(f'Ваш пароль длинной в {lengths} символов готов:', result_str)

welcome_skript()

user_length = int(input('Введите длину пароля: '))
length = user_length
letters = string.ascii_lowercase

user_set_pass1 = input('Хотите ли вы чтобы в вашем пароле были заглавные буквы? \nДа\\нет: ').lower()
if user_set_pass1 == "да":
    letters = string.ascii_letters
user_set_pass2 = input('Хотите ли вы чтобы в вашем пароле были цифры? \nДа\\нет: ').lower()
if user_set_pass2 == "да":
    letters = string.ascii_letters + string.digits
user_set_pass3 = input('Хотите ли вы чтобы в вашем пароле были специальные символы? \nДа\\нет: ').lower()
if user_set_pass3 == "да":
    letters = string.ascii_letters + string.digits + string.punctuation

print()
print("Начинаю генерацию пароля!")
get_random_password(length, letters)

print()
input("Чтобы завершить работу программы нажмите enter ")
