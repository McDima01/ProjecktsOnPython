import schedule
import time
import threading
from bot import post_random_track, bot

def start_schedule():
    schedule.every(1).hours.do(post_random_track)
    bot.send_message(5038901733, "Начинаю пост треков каждый час")
    print("Начинаю пост треков каждый час")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=start_schedule).start()
