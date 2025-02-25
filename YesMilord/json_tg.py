import json

# Пример загрузки данных пользователя
def load_user_data():
    with open('user_data.json', 'r') as file:
        return json.load(file)

def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_user_data(user_id):
    user_data = load_user_data()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "money": 50,
            "influence": 50,
            "level": 0,  # Уровень по умолчанию
            "wins": 0,
            "losses": 0,
        }
        save_user_data(user_data)
    # Убедитесь, что все ключи присутствуют
    user_data[str(user_id)].setdefault("level", 0)
    return user_data[str(user_id)], user_data

def update_user_data(user_id, updates):
    try:
        user_data = load_user_data()
        if str(user_id) in user_data:
            for key, value in updates.items():
                user_data[str(user_id)][key] = value
            save_user_data(user_data)
            print(f"Обновлено: {user_data[str(user_id)]}")
        else:
            print("Пользователь не найден.")
    except Exception as e:
        print(f"Ошибка при обновлении данных: {e}")

def reset_user_data(user_id):
    """Сбрасывает данные пользователя до начальных значений."""
    try:
        user_data = load_user_data()
        if str(user_id) in user_data:
            user_data[str(user_id)] = {
                "money": 50,
                "influence": 50,
                "level": 0,
                "wins": user_data[str(user_id)].get("wins", 0),  # Оставляем счётчик побед
                "losses": user_data[str(user_id)].get("losses", 0),  # Оставляем счётчик поражений
                "selected_event": None,  # Сброс события
            }
            save_user_data(user_data)
            print(f"Данные пользователя {user_id} сброшены.")
        else:
            print(f"Пользователь {user_id} не найден, сброс невозможен.")
    except Exception as e:
        print(f"Ошибка при сбросе данных пользователя: {e}")
