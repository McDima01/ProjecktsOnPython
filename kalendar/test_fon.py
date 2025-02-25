import shutil
import subprocess
import sys
import time
import getpass
from kalendar import present_times

DETACHED_PROCESS = 0x00000008
username = getpass.getuser()
filename = 'fon.exe'  # путь до файла
dir_name = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'

def copy_to_autodownload():
    shutil.copy(filename, dir_name)

def start_program():

    while True:
        # Отсоединяем процесс от консоли
        if sys.platform == 'win32':
            command = present_times()
            if command is not None:  # Проверяем, что команда не None
                subprocess.Popen(command, creationflags=DETACHED_PROCESS)
'''                time.sleep(1800)'''

start_program()
