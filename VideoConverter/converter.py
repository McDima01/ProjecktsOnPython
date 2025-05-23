import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os
import threading

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MKV → AVI Конвертер (5.1 Аудио)")
        self.root.geometry("450x250")

        self.input_path = ""
        self.output_folder = ""

        # Виджеты
        self.label = tk.Label(root, text="Выберите .mkv файл:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.select_file_button = tk.Button(root, text="Выбрать видео", command=self.select_file)
        self.select_file_button.pack()

        self.select_folder_button = tk.Button(root, text="Выбрать папку сохранения", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        self.convert_button = tk.Button(root, text="Конвертировать", command=self.start_conversion)
        self.convert_button.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=300)
        self.progress.pack(pady=10)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("MKV файлы", "*.mkv")])
        if path:
            self.input_path = path
            self.label.config(text=f"Файл: {os.path.basename(path)}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder

    def start_conversion(self):
        if not self.input_path:
            messagebox.showwarning("Нет файла", "Выберите .mkv файл.")
            return
        if not self.output_folder:
            messagebox.showwarning("Нет папки", "Выберите папку для сохранения.")
            return
        threading.Thread(target=self.convert_video).start()

    def convert_video(self):
        self.progress.start()
        output_filename = os.path.splitext(os.path.basename(self.input_path))[0] + '.avi'
        output_path = os.path.join(self.output_folder, output_filename)

        # Используем первую аудиодорожку (0:a:0)
        command = [
            'ffmpeg',
            '-i', self.input_path,
            '-map', '0:v:0',  # первая видеодорожка
            '-map', '0:a:0',  # первая аудиодорожка
            '-c:v', 'mpeg4',
            '-qscale:v', '2',
            '-c:a', 'ac3',
            '-ac', '6',
            output_path
        ]

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Готово", f"Файл сохранён:\n{output_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Ошибка при конвертации:\n{e}")
        finally:
            self.progress.stop()

# Запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
