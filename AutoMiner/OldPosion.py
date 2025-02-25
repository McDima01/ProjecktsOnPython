import pyautogui
from time import sleep
import pydirectinput

pix = -431

pyautogui.hotkey("alt", "tab")

sleep(2)

def teleport():
    pyautogui.press("m")
    sleep(0.5)
    pydirectinput.moveRel(280, 180)
    sleep(0.5)
    pyautogui.click()
    sleep(0.5)

def go_to_mine():
    # Зажимаем W и ПКМ
    pyautogui.keyDown("w")
    pyautogui.keyDown("d")

    # Держим 3 секунды
    sleep(1.25)

    # Отпускаем W и ПКМ
    pyautogui.keyUp("w")
    pyautogui.keyUp("d")
    pydirectinput.moveRel(0, 5000)
    sleep(1)
    pyautogui.mouseDown(button="left")
    pyautogui.keyDown("s")
    sleep(0.5)
    pyautogui.mouseUp(button="left")
    pyautogui.keyUp("s")

def mine():
    pyautogui.keyDown("w")
    pyautogui.mouseDown(button="left")
    sleep(10)
    pyautogui.keyUp("w")
    pyautogui.mouseUp(button="left")

def down_and_revers():
    pydirectinput.moveRel(0, 5000)
    pyautogui.mouseDown(button="left")
    sleep(0.5)
    pyautogui.mouseUp(button="left")
    pydirectinput.moveRel(1200, pix)



teleport()
go_to_mine()
pydirectinput.moveRel(0, pix)

while True:
    mine()
    # down_and_revers()
    """    mine()
    down_and_revers()
    mine()
    down_and_revers()
    mine()
    down_and_revers()
    mine()
    down_and_revers()
    mine()
    down_and_revers()"""
    teleport()
    go_to_mine()
    sleep(0.1)
    pydirectinput.moveRel(0, pix)
