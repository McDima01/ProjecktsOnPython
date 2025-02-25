import requests
import os
import random
import re
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
import yandex_music
from config import DOWNLOAD_DIR, YANDEX_TOKEN  # Путь загрузки берётся из config.py

# Авторизация
client = yandex_music.Client(YANDEX_TOKEN).init()

def get_id_from_url(url):
    """Определяет, является ли ссылка плейлистом или альбомом, и возвращает (тип, ID)."""
    playlist_match = re.search(r'playlists/(\d+)', url)
    album_match = re.search(r'album/(\d+)', url)

    if playlist_match:
        return "playlist", playlist_match.group(1)
    elif album_match:
        return "album", album_match.group(1)
    return None, None


def download_track(track, cover_path):
    """Скачивает трек, обложку и встраивает метаданные."""
    track_name = f"{track.artists[0].name} - {track.title}.mp3"
    track_path = os.path.join(DOWNLOAD_DIR, track_name)

    # Скачивание трека
    track.download(track_path)

    # Добавление метаданных (обложки и тегов)
    audio = MP3(track_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    # Встраивание обложки в метаданные
    audio.tags.add(
        APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=open(cover_path, "rb").read(),
        )
    )
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artists[0].name))
    audio.save()

    print(f"✅ Трек '{track_name}' с обложкой '{cover_path}' скачан и сохранён в '{DOWNLOAD_DIR}'")
    return track_path


    # Скачивание обложки
    cover_url = track.cover_uri.replace("%%", "1000x1000")
    response = requests.get(f"https://{cover_url}")
    with open(cover_path, "wb") as f:
        f.write(response.content)

    # Добавление метаданных (обложки и тегов)
    audio = MP3(track_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(
        APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=open(cover_path, "rb").read(),
        )
    )
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artists[0].name))
    audio.save()

    print(f"✅ Трек '{track_name}' скачан и сохранён в '{DOWNLOAD_DIR}'")
    return track_path


def get_user_preference(user_id):
    """Читает предпочтение пользователя из файла user_data.json по user_id."""
    try:
        with open("user_data.json", "r") as f:
            data = json.load(f)
            user_data = data.get(str(user_id))  # Получаем настройки для конкретного пользователя
            if user_data:
                return user_data.get("random_order", False)  # Вернёт True, если порядок случайный, иначе False
            else:
                print("❌ Данные пользователя не найдены.")
                return False
    except FileNotFoundError:
        print("❌ Файл user_data.json не найден.")
        return False


def download_cover(track):
    """Скачивает обложку для трека."""
    cover_name = f"{track.artists[0].name} - {track.title}.jpg"
    cover_path = os.path.join(DOWNLOAD_DIR, cover_name)

    # Скачивание обложки
    cover_url = track.cover_uri.replace("%%", "1000x1000")  # Получаем ссылку на обложку с нужным разрешением
    response = requests.get(f"https://{cover_url}")
    with open(cover_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Обложка для трека '{track.title}' сохранена в '{cover_path}'")
    return cover_path

def get_random_track(url, user_id=None):
    """Определяет источник (плейлист или альбом), получает случайный или по порядку трек и скачивает его."""
    media_type, media_id = get_id_from_url(url)

    if media_type == "playlist":
        playlist = client.playlist(media_id)  # Получаем плейлист по ID
        tracks = [track.track for track in playlist.tracks]
        print(f"🎵 Выбран плейлист: {playlist.title}")

    elif media_type == "album":
        album = client.albums_with_tracks(media_id)
        tracks = [track for volume in album.volumes for track in volume]  # Объединяем все диски в альбоме
        print(f"🎶 Выбран альбом: {album.title} - {album.artists[0].name}")

    else:
        print("❌ Ошибка: Не удалось определить тип ссылки.")
        return

    # Чтение настройки о случайном порядке треков для пользователя
    shuffle = get_user_preference(user_id) if user_id else False  # если user_id нет, то не случайный порядок

    if shuffle:
        # Если случайный порядок
        track = random.choice(tracks)
        print(f"🔹 Выбран случайный трек: {track.title} - {', '.join(artist.name for artist in track.artists)}")
    else:
        # Если по порядку
        track = tracks[0]  # Например, выбираем первый трек
        print(f"🔹 Выбран трек по порядку: {track.title} - {', '.join(artist.name for artist in track.artists)}")

    # Скачивание обложки
    cover_path = download_cover(track)

    # Скачивание трека и добавление метаданных
    download_track(track, cover_path)



"""# Пример использования с user_id
user_id = 5038901733  # Замените на user_id пользователя
url = "https://music.yandex.ru/album/123456"  # Замените на нужную ссылку

# Запуск скачивания трека
get_random_track(url, user_id)
"""