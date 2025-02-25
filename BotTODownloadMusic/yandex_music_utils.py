import os
import re
import requests
import yandex_music
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from config import YANDEX_TOKEN, DOWNLOAD_DIR

client = yandex_music.Client(YANDEX_TOKEN).init()


def get_track(track):
    track_name = f"{track.artists[0].name} - {track.title}.mp3"
    track_path = os.path.join(DOWNLOAD_DIR, track_name)

    cover_name = f"{track.artists[0].name} - {track.title}.jpg"
    cover_path = os.path.join(DOWNLOAD_DIR, cover_name)

    # Скачивание трека
    track.download(track_path)

    # Скачивание обложки
    cover_url = track.cover_uri.replace('%%', '1000x1000')
    response = requests.get(f"https://{cover_url}")
    with open(cover_path, 'wb') as f:
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
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=open(cover_path, 'rb').read(),
        )
    )
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artists[0].name))
    audio.save()

    return track_path, cover_path


def get_playlist_tracks(url):
    try:
        playlist_match = re.search(r"users/([^/]+)/playlists/(\d+)", url)
        album_match = re.search(r"album/(\d+)", url)

        if playlist_match:
            username, playlist_id = playlist_match.groups()
            playlist = client.users_playlists(user_id=username, kind=int(playlist_id))
            if not playlist:
                print(f"Плейлист с ID {playlist_id} не найден.")
                return []
            return [track for track in playlist.tracks]

        elif album_match:
            album_id = album_match.group(1)
            album = client.albums_with_tracks(album_id)
            if not album:
                print(f"Альбом с ID {album_id} не найден.")
                return []
            print(f"Альбом найден: {album.title}")
            return [track for volume in album.volumes for track in volume]

        else:
            print(f"Не удалось извлечь данные из URL: {url}")
            return []

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []



"""import requests
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from config import DOWNLOAD_DIR, YANDEX_TOKEN
import yandex_music

client = yandex_music.Client(YANDEX_TOKEN).init()


def get_track(track):
    track_name = f"{track.artists[0].name} - {track.title}.mp3"
    track_path = os.path.join(DOWNLOAD_DIR, track_name)

    cover_name = f"{track.artists[0].name} - {track.title}.jpg"
    cover_path = os.path.join(DOWNLOAD_DIR, cover_name)

    # Скачивание трека
    track.download(track_path)

    # Скачивание обложки
    cover_url = track.cover_uri.replace('%%', '1000x1000')
    response = requests.get(f"https://{cover_url}")
    with open(cover_path, 'wb') as f:
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
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=open(cover_path, 'rb').read(),
        )
    )
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artists[0].name))
    audio.save()

    return track_path, cover_path

"""
