import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import sys
import os
import re
import shutil
import subprocess
from threading import Thread

from src.subtitles.handle_video import HandleVideo


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Прокрутка вниз


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("auto-subs")

        self.root.geometry("600x400")

        self.text_widget = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=40, height=10)
        self.text_widget.pack(expand=True, fill="both")

        console_redirector = ConsoleRedirector(self.text_widget)
        sys.stdout = console_redirector

        self.file_path = None

        self.file_button = tk.Button(
            self.root, text="Выбрать файл", command=self.choose_file)
        self.file_button.pack()

        self.directory_path = None

        self.dir_button = tk.Button(
            self.root, text="Выбрать директорию", command=self.choose_directory)
        self.dir_button.pack()


    def execute(self):
        if os.path.exists('./bin') and os.path.isdir('./bin'):
            shutil.rmtree('./bin')

        os.mkdir('./bin')
        Thread(target=self.process_file, daemon=True).start()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            print(f"Выбран файл: {self.file_path}")
            if self.directory_path:
                self.execute()
            else:
                print("Директория не выбрана")
        else:
            print("Файл не выбран")

    def choose_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            print(f"Выбрана директория: {self.directory_path}")
            if self.file_path:
                self.execute()
            else:
                print("Файл не выбран")
        else:
            print("Директория не выбрана")

    @staticmethod
    def clear_bin_directory(path):
        bin_directory = path

        try:
            for file_name in os.listdir(bin_directory):
                file_path = os.path.join(bin_directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        except Exception as e:
            print(f"Произошла ошибка при удалении файлов с субтитрами: {e}")

    def process_file(self):
        if self.file_path and self.directory_path:
            try:
                base_dir = os.path.abspath(os.path.dirname(__file__))
                base_dir = re.sub(r'\\', '/', base_dir)
                os.environ['PROJECT_ROOT'] = base_dir

                model = 'small'

                process_whisper = subprocess.Popen(
                    f'cd {base_dir}/bin && whisper {self.file_path} --model {model} --language en',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                for line in process_whisper.stdout:
                    print(line.strip())
                    
                process_handle_video = subprocess.Popen(
                    
                    # ['python', '-c', f'from main import HandleVideo; HandleVideo.handle_video("{self.file_path.split("/")[-1]}", "{self.file_path}", "{self.directory_path}")'],
                    
                    ['python', '-c', f'from src.subtitles.handle_video import HandleVideo; HandleVideo.handle_video("{self.file_path.split("/")[-1]}", "{self.file_path}", "{self.directory_path}")'],
                    
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                for line in process_handle_video.stdout:
                    print(line.strip())

                process_whisper.wait()
                process_handle_video.wait()

                self.clear_bin_directory('./bin')
                os.rmdir('./bin')

            except Exception as e:
                print(f"Произошла ошибка: {e}")
        else:
            print("Необходимо выбрать файл и директорию для продолжения обработки.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()
