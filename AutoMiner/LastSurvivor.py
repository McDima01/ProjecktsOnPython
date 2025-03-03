#region Сбор данных
"""import pyautogui
import keyboard
import time
import cv2
import numpy as np
import pandas as pd
import os
import mouse
import mss

# Папка для сохранения данных
SAVE_DIR = "screenshots"
os.makedirs(SAVE_DIR, exist_ok=True)

# Файл для хранения меток
LABELS_FILE = "labels.csv"

# Проверяем, есть ли уже разметка
if os.path.exists(LABELS_FILE):
    df = pd.read_csv(LABELS_FILE)
    labels_data = df.values.tolist()
    count = len(df)  # Продолжаем с последнего сохраненного индекса
    print(f"Продолжаем разметку с {count}-го снимка...")
else:
    labels_data = []
    count = 0
    print("Начинаем новую разметку...")

# Начальная задержка между снимками
screenshot_delay = 0.4
prev_mouse_x, prev_mouse_y = pyautogui.position()
scroll_detected = False

def on_scroll(event):
    global scroll_detected
    if hasattr(event, "delta") and event.delta != 0:
        scroll_detected = True

mouse.hook(on_scroll)  # Подключаем обработчик событий мыши

def capture_screen():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        return np.array(screenshot)

def save_data(image, action, count):
    filename = f"{SAVE_DIR}/screenshot_{count}.png"
    cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    labels_data.append([filename, action])

print("Запись началась! Нажми 'p' для выхода. '+' - ускорить, '-' - замедлить.")

while True:
    actions = []
    image = capture_screen()

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

    if scroll_detected:
        actions.append("scroll_wheel")
        scroll_detected = False  # Сбрасываем флаг после фиксации прокрутки

    mouse_x, mouse_y = pyautogui.position()
    if (mouse_x, mouse_y) != (prev_mouse_x, prev_mouse_y):
        actions.append(f"mouse_move ({mouse_x}, {mouse_y})")
        prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

    if actions:
        save_data(image, ", ".join(actions), count)
        print(f"Сохранено: {count} -> {actions}")
        count += 1

    if keyboard.is_pressed('+'):
        screenshot_delay = max(0.05, screenshot_delay - 0.05)
        print(f"Ускорение: {screenshot_delay:.2f} сек")
        time.sleep(0.2)

    if keyboard.is_pressed('-'):
        screenshot_delay = min(2, screenshot_delay + 0.05)
        print(f"Замедление: {screenshot_delay:.2f} сек")
        time.sleep(0.2)

    if keyboard.is_pressed('p'):
        break

    time.sleep(screenshot_delay)

# Сохранение меток (добавляем новые данные к старым)
df = pd.DataFrame(labels_data, columns=["image_path", "label"])
df.to_csv(LABELS_FILE, index=False)

print("Разметка завершена. Данные сохранены в", LABELS_FILE)
mouse.unhook_all()
"""
#endregion

#region Подготовка данных
"""import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from collections import Counter

# Загружаем разметку
df = pd.read_csv("labels.csv")

# Проверяем, нет ли пустых строк и битых данных
df = df.dropna()
df = df[df["image_path"].apply(lambda x: x.endswith(".png") or x.endswith(".jpg"))]

# Словарь {действие -> индекс}
actions = ["move_forward", "move_left", "move_backward", "move_right",
           "select_perk_1", "select_perk_2", "select_perk_3", "select_perk_4",
           "right_click", "left_click", "scroll_wheel"]
action_to_index = {action: i for i, action in enumerate(actions)}

# Функция для преобразования меток в индексы с обработкой ошибок
def convert_to_index(label_str):
    result = []
    for action in label_str.split(", "):
        try:
            result.append(action_to_index[action])
        except KeyError:
            # Выводим ошибочную метку
            print(f"Неизвестная метка: {action}")
            # Если метка неизвестна, можно заменить её на -1 (или просто пропустить)
            result.append(-1)
    return result

# Преобразуем текстовые метки в числа с обработкой ошибок
df["label"] = df["label"].apply(convert_to_index)

# Удаляем строки с неправильными метками (-1)
df = df[df["label"].apply(lambda x: -1 not in x)]

# Загружаем изображения и метки
X = []
y = []

for index, row in df.iterrows():
    img = cv2.imread(row["image_path"])  # Открываем картинку
    img = cv2.resize(img, (224, 224))  # Меняем размер
    img = img / 255.0  # Нормализация (от 0 до 1)

    X.append(img)

    # Создаём вектор действий (0 и 1)
    label_vector = np.zeros(len(actions))
    for action_index in row["label"]:
        label_vector[action_index] = 1
    y.append(label_vector)

# Преобразуем в массивы NumPy
X = np.array(X)
y = np.array(y)

# Проверяем баланс данных
all_labels = []
for label_list in df["label"]:
    all_labels.extend(label_list)
label_counts = Counter(all_labels)
print("Частота кнопок:", label_counts)

# Разделяем на обучающую (80%) и тестовую (20%) выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("✅ Данные готовы! X_train.shape:", X_train.shape)"""
#endregion

#region Создание нейронки
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import cv2
import re
import pandas as pd
from collections import Counter

# Список действий
actions = ["move_forward", "move_left", "move_backward", "move_right",
           "select_perk_1", "select_perk_2", "select_perk_3", "select_perk_4",
           "right_click", "left_click", "scroll_wheel"]

# Словарь для преобразования действий в индексы
action_to_index = {action: i for i, action in enumerate(actions)}

# Загружаем разметку
df = pd.read_csv("labels.csv")

# Функция для корректного разделения меток
def parse_labels(label_str):
    actions_list = []
    mouse_x, mouse_y = None, None  # Координаты мыши (если есть)

    matches = re.findall(r'([a-zA-Z_]+(?: \(\d+, \d+\))?)', label_str)

    for match in matches:
        if "mouse_move" in match:  # Если это движение мыши
            coords = re.findall(r'\d+', match)  # Извлекаем числа
            if len(coords) == 2:
                mouse_x, mouse_y = int(coords[0]), int(coords[1])  # Записываем координаты
        elif match in action_to_index:
            actions_list.append(action_to_index[match])  # Конвертируем в индекс
        else:
            actions_list.append(match)  # На всякий случай, но не должно быть

    return actions_list, mouse_x, mouse_y

# Применяем функцию
df[["image_path", "label"]] = df["label"].str.split(",", n=1, expand=True)
df["image_path"] = df["image_path"].str.strip()
df["label"] = df["label"].str.strip()

df[["actions", "mouse_x", "mouse_y"]] = df["label"].apply(lambda x: pd.Series(parse_labels(x)))

# Заменяем NaN на 0 (если нет движения мыши)
df["mouse_x"] = df["mouse_x"].fillna(0).astype(int)
df["mouse_y"] = df["mouse_y"].fillna(0).astype(int)

# Загружаем изображения и метки
X = []  # Изображения
y = []  # Метки

for index, row in df.iterrows():
    img = cv2.imread(row["image_path"])  # Открываем картинку
    img = cv2.resize(img, (224, 224))  # Меняем размер
    img = img / 255.0  # Нормализация

    X.append(img)

    # Создаём вектор для метки
    label_vector = np.zeros(len(actions))
    for action_index in row["label"]:
        label_vector[action_index] = 1
    y.append(label_vector)

# Преобразуем в массивы NumPy
X = np.array(X)
y = np.array(y)

# Разделяем на обучающую и тестовую выборку
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Подсчитываем частоту классов и вычисляем веса
all_labels = []
for label_list in df["label"]:
    all_labels.extend(label_list)
label_counts = Counter(all_labels)
class_weights = compute_class_weight('balanced', classes=np.unique(np.argmax(y_train, axis=1)), y=np.argmax(y_train, axis=1))

# Создание модели нейросети
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(actions), activation='sigmoid')  # 11 выходов (по числу действий)
])

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), class_weight=class_weights)

# Сохраняем модель
model.save("minecraft_bot.h5")

# Оценка модели на тестовых данных
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"✅ Тестовая точность: {test_accuracy:.2f}")
print(f"✅ Тестовая потеря: {test_loss:.2f}")
#endregion