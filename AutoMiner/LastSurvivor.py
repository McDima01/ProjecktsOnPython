import pyautogui
import keyboard
import time
import cv2
import numpy as np
import pandas as pd
import os
from pynput.mouse import Listener

# Папка для сохранения данных
SAVE_DIR = "screenshots"
os.makedirs(SAVE_DIR, exist_ok=True)

# Файл для хранения меток
LABELS_FILE = "labels.csv"
labels_data = []

# Начальная задержка между снимками
screenshot_delay = 0.4

# Переменные для отслеживания движения мыши
prev_mouse_x, prev_mouse_y = pyautogui.position()
scroll_detected = False

# Функция обработки прокрутки колесика
def on_scroll(x, y, dx, dy):
    global scroll_detected

    scroll_detected = True

# Запускаем слушатель мыши
mouse_listener = Listener(on_scroll=on_scroll)
mouse_listener.start()

# Функция для захвата экрана
def capture_screen():
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)

# Функция для сохранения данных
def save_data(image, action, count):
    filename = f"{SAVE_DIR}/screenshot_{count}.png"
    cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    labels_data.append([filename, action])

# Основной цикл сбора данных
count = 0
print("Запись началась! Нажми 'p' для выхода. '+' - ускорить, '-' - замедлить.")

while True:
    actions = []  # Очищаем список действий перед каждым циклом
    image = capture_screen()  # Делаем скриншот перед сохранением данных

    # Отслеживание клавиш
    if keyboard.is_pressed("w"): actions.append("move_forward")
    if keyboard.is_pressed("a"): actions.append("move_left")
    if keyboard.is_pressed("s"): actions.append("move_backward")
    if keyboard.is_pressed("d"): actions.append("move_right")
    if keyboard.is_pressed("1"): actions.append("select_perk_1")
    if keyboard.is_pressed("2"): actions.append("select_perk_2")
    if keyboard.is_pressed("3"): actions.append("select_perk_3")
    if keyboard.is_pressed("4"): actions.append("select_perk_4")
    if keyboard.is_pressed("right"): actions.append("right_click")
    if keyboard.is_pressed("left"): actions.append("left_click")

    # Проверяем флаг прокрутки колесика
    if scroll_detected:
        actions.append("scroll_wheel")
        scroll_detected = False  # Сбрасываем флаг после фиксации прокрутки

    # Отслеживание движения мыши
    mouse_x, mouse_y = pyautogui.position()
    if (mouse_x, mouse_y) != (prev_mouse_x, prev_mouse_y):
        actions.append(f"mouse_move ({mouse_x}, {mouse_y})")
        prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

    # Сохранение данных, если есть действие
    if actions:
        save_data(image, ", ".join(actions), count)
        print(f"Сохранено: {count} -> {actions}")
        count += 1

    # Изменение скорости скриншотов
    if keyboard.is_pressed('+'):
        screenshot_delay = max(0.05, screenshot_delay - 0.05)  # Минимум 0.05 сек
        print(f"Ускорение: {screenshot_delay:.2f} сек")
        time.sleep(0.2)  # Защита от слишком быстрого нажатия

    if keyboard.is_pressed('-'):
        screenshot_delay = min(2, screenshot_delay + 0.05)  # Максимум 2 сек
        print(f"Замедление: {screenshot_delay:.2f} сек")
        time.sleep(0.2)

    # Выход из программы
    if keyboard.is_pressed('p'):
        break

    time.sleep(screenshot_delay)

# Сохранение меток
df = pd.DataFrame(labels_data, columns=["image_path", "label"])
df.to_csv(LABELS_FILE, index=False)

print("Разметка завершена. Данные сохранены в", LABELS_FILE)

# Останавливаем слушатель мыши перед выходом
mouse_listener.stop()
