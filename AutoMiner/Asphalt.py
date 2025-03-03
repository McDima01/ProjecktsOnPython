import pyautogui
from time import sleep
import pydirectinput

pix = -431

pyautogui.hotkey("alt", "tab")

sleep(2)

pydirectinput.moveRel(0, 0)