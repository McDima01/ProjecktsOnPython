import pyautogui
from time import sleep
import pydirectinput
trueOrFalse = True


print("This на самом деле working")

# Переключаем окно
pyautogui.hotkey("alt", "tab")

# Даем системе время переключить окно
sleep(5)

"""# Получаем размеры экрана
screen_width, screen_height = pyautogui.size()

pydirectinput.moveRel(0, 5000)

# Перемещаем мышь в центр экрана
pydirectinput.moveTo(screen_width // 2, screen_height // 2)
"""
def mouse_work():
    global trueOrFalse
    if trueOrFalse == True:
        pydirectinput.moveRel(0, -1)
        trueOrFalse = False
    else:
        pydirectinput.moveRel(0, 1)
        trueOrFalse = True


while True:
    """pyautogui.keyDown("enter")
    sleep(0.5)
    pyautogui.keyUp("enter")"""
    pyautogui.press("enter")
    sleep(40)
    mouse_work()
    pyautogui.click()
    sleep(7)
    pyautogui.press("enter")
    sleep(5)
    pyautogui.press("enter")
    sleep(5)

