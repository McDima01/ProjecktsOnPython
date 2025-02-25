"""
6. Календарь
   Разработайте программу, которая отображает текущий месяц и позволяет пользователю добавлять события.
"""
import time
from notifypy import Notify
import test_fon


numb = 0

def welcome_skript():
    print('Приветствую! \nЭто календарь, в котором можно посмотреть дату и добавить событие.')
    input("Чтобы продолжить нажмите enter ")

def name_day(day):
    if day == 'Mon':
        day = "Понедельник"
    elif day == 'Tue':
        day = 'Вторник'
    elif day == 'Wed':
        day = 'Среда'
    elif day == 'Thy':
        day = 'Четверг'
    elif day == 'Fri':
        day = 'Пятница'
    elif day == 'Sat':
        day = 'Суббота'
    elif day == 'Sun':
        day = 'Воскресенье'
    else:
        print("Ты что-то сделал не так :(")
    return day

def name_month(month):
    if month == 'Jan':
        monthh = "январь"
    elif month == 'Feb':
        monthh = 'Февраль'
    elif month == 'Mar':
        monthh = 'Март'
    elif month == 'Apr':
        monthh = 'Апрель'
    elif month == 'May':
        monthh = 'Maй'
    elif month == 'Jun':
        monthh = 'Июнь'
    elif month == 'Jul':
        monthh = 'Июль'
    elif month == 'Aug':
        monthh = 'Август'
    elif month == 'Sept':
        monthh = 'Сентябрь'
    elif month == 'Oct':
        monthh = 'Октябрь'
    elif month == 'Nov':
        monthh = 'Ноябрь'
    elif month == 'Dec':
        monthh = 'Декабрь'
    else:
        print("Ты что-то сделал не так :(")
    return monthh

def split_data():
    time_parts = time.asctime().split(" ")
    dayy = time_parts[0]
    monthh = time_parts[1]
    day_numberr = time_parts[2]
    present_timee = time_parts[3]
    yearr = time_parts[4]
    return dayy, monthh, day_numberr, present_timee, yearr

day, month, day_number, present_time, year = split_data()
parts_time = present_time.split(":")
hour = parts_time[0]
minute = parts_time[1]
seconds = parts_time[2]

def present_times():
    global numb
    notification = Notify()
    notification.title = "Сейчас:"
    notification.message = (f'День недели - {name_day(day)}, число - {day_number}, месяц - {name_month(month)}, год - {year}, '
                            f'время - {hour}:{minute}')
    notification.send()
    numb += 1
    print(numb)
    time.sleep(1800)

'''if __name__ == "__main__":
    test_fon.copy_to_autodownload()
    test_fon.start_program()
'''
