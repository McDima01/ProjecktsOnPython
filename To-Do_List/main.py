"""3. Простой список дел (to-do list)
Программа позволяет добавлять, удалять и просматривать задачи. Пользователь вводит команды,
а программа хранит список задач в памяти во время работы."""
import os

task_list = {}  # список задач
number = 0
task = None
file_name = "To_Do_List.txt"
file_path = os.path.join(os.getcwd(), file_name)

def create_file(file_path, user_task_list):
    try:
        with open(file_path, "w") as file:
            file.write(user_task_list)
        print(f'Файл {file_name} был успешно создан в {file_path}')
    except Exception as e:
        print(f"Произошла ошибка при создании файла: {e}")


def create_task(task_list, task, number):
    if number in task_list:
        print()
        print('Вы уже добавили задание с таким же номером')
    else:
        task_list[number] = task  # Добавление новой задачи в словарь
        print(f"Задание \"{task}\" добавлено успешно!")
        print(task_list)

    return task_list


def delete_task(task_list, number):
     if number in task_list:
        print(f"Задание \"{task_list[number]}\" удалено успешно!")
        del task_list[number]
     else:
         print()
         print(f'Задание с номером {number} не существует')
     return task_list

 # task_list = create_task(task_list, task, number)

# create_task(task_list, task, number)

while True:
    user_task_list = str(task_list).replace("{", "").replace("}", "").replace("'", "")
    print()
    if len(task_list) == 0:
        print('Вы еще ничего не добавили в список дел.')
    else:
        print(f'Список дел: {user_task_list}')
    print(f'Чтобы добавить дело к списку введите команду: добавить')
    print(f'Чтобы удалить дело из списка напишите: удалить')
    print(f'Чтобы создать файл с вашим списком дел напишите: файл')
    print('Чтобы выйти напишите: выйти')
    command = input('Введите команду: ')
    if command == "добавить":
        try:
            print()
            print("Чтобы добавить дело введите его в таком формате: \n1(номер дела) : дело(которое нужно сделать)")
            pre_task = input(f'Введите задание в выше указанном формате: ').split(' : ', 1)
            number = str(pre_task[0])
            task = pre_task[1]
            task_list = create_task(task_list, task, number)
        except IndexError:
            print()
            print('Вы ввели не в правильном формате')
            print('Обязательно вводите ":" через пробел " : " ')

    elif command == 'удалить':
        print()
        print(f'Чтобы удалить дело из списка введите его номер.')
        number = str(input('Введите номер дела которое хотите удалить: '))
        task_list = delete_task(task_list, number)
    elif command == 'файл':
        print()
        create_file(file_path, user_task_list)
    elif command == 'выйти':
        print()
        print()
        print('Программа завершила работу')
        break
    else:
        print()
        print('Вы ввели не правильную команду')

