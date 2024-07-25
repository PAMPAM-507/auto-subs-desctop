import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter.ttk import Combobox
import sys
import os
import re
import shutil
import subprocess
import re
from threading import Thread
import whisper


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("auto-subs")
        self.root.geometry("650x470")

        self.text_widget = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=75, height=15)
        self.text_widget.grid(row=0, column=0, columnspan=4, sticky="nsew")

        console_redirector = ConsoleRedirector(self.text_widget)
        sys.stdout = console_redirector

        self.file_path = None
        self.directory_path = None
        self.model_var = tk.StringVar(value='tiny')
        self.translate_var = tk.BooleanVar(value=False)

        self.file_button = tk.Button(
            self.root, text="     Select a file     ", command=self.choose_file)
        self.file_button.grid(row=1, column=0, padx=10, pady=10)

        self.dir_button = tk.Button(
            self.root, text="Select a directory", command=self.choose_directory)
        self.dir_button.grid(row=2, column=0, padx=10, pady=10)

        self.model_label = tk.Label(self.root, text="Select model:")
        self.model_label.grid(row=1, column=2, padx=10, pady=10)

        self.model_combobox = Combobox(
            self.root, values=['tiny', 'base', 'small', 'medium', 'large'], textvariable=self.model_var)
        self.model_combobox.grid(row=1, column=3, padx=10, pady=10)

        self.model_description_label = tk.Label(self.root, text="", wraplength=400, justify=tk.LEFT)
        self.model_description_label.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

        self.translate_checkbutton = tk.Checkbutton(
            self.root, text="Translate audio", variable=self.translate_var)
        self.translate_checkbutton.grid(row=3, column=3, columnspan=2, pady=10)

        self.execute_button = tk.Button(
            self.root, text="Execute", command=self.execute)
        self.execute_button.grid(row=7, column=0, columnspan=4, pady=10)

        self.model_descriptions = {
            'tiny': 'Tiny model description: English-only model; Required VRAM: ~1 GB; Relative speed: ~32x.',
            'base': 'Base model description: English-only model; Required VRAM: ~1 GB; Relative speed: ~16x.',
            'small': 'Small model description: English-only model; Required VRAM: ~2 GB; Relative speed: ~6x.',
            'medium': 'Medium model description: English-only model; Required VRAM: ~5 GB; Relative speed: ~2x.',
            'large': 'Large model description: Any popular language; Required VRAM: ~10 GB; Relative speed: 1x.',
        }

        self.update_model_description(None)
        self.model_combobox.bind("<<ComboboxSelected>>", self.update_model_description)

    def update_model_description(self, event):
        selected_model = self.model_var.get()
        description = self.model_descriptions.get(selected_model, "")
        self.model_description_label.config(text=description)

    def execute(self):
        try:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            base_dir = re.sub(r'\\', '/', base_dir)
            os.environ['PROJECT_ROOT'] = base_dir

            if not(os.path.exists(os.path.join(base_dir, 'src/subtitles/model/')) and os.path.isdir(os.path.join(base_dir, 'src/subtitles/model/'))):
                from pathlib import Path
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

                model_name = "Helsinki-NLP/opus-mt-en-ru"

                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

                tokenizer.save_pretrained(Path.cwd() / 'src' / 'subtitles' / 'model' / 'en-ru-local')
                model.save_pretrained(Path.cwd() / 'src' / 'subtitles' / 'model' / 'en-ru-local')

            if os.path.exists('./bin') and os.path.isdir('./bin'):
                shutil.rmtree('./bin')

            os.mkdir('./bin')
            Thread(target=self.process_file, daemon=True).start()
        except Exception as e:
            print(f"Error during initialization: {e}")

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            print(f"The file is selected: {self.file_path}")
        else:
            print("The file is not selected")

    def choose_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            print(f"A directory has been selected: {self.directory_path}")
        else:
            print("The directory is not selected")

    @staticmethod
    def clear_bin_directory(path):
        bin_directory = path

        try:
            for file_name in os.listdir(bin_directory):
                file_path = os.path.join(bin_directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        except Exception as e:
            print(f"An error occurred when deleting files with subtitles: {e}")

    def process_file(self):
        if self.file_path and self.directory_path:
            # try:
            base_dir = os.environ.get('PROJECT_ROOT')

            model = self.model_var.get()
            translate = self.translate_var.get()
            print('You chose model: ', model)
            print('Translate audio: ', translate)

            from src.utils.progress_bar import _CustomProgressBar, _CustomProgressBarForHandleVideo
            from src.utils.make_srt import MakingSrt
            import whisper.transcribe
            transcribe_module = sys.modules['whisper.transcribe']

            import contextlib

            @contextlib.contextmanager
            def temporary_tqdm_replacement():
                original_tqdm = transcribe_module.tqdm.tqdm
                transcribe_module.tqdm.tqdm = _CustomProgressBar
                try:
                    yield
                finally:
                    transcribe_module.tqdm.tqdm = original_tqdm

            # model = whisper.load_model(model)
            # result = model.transcribe(self.file_path, language='en', fp16=False, verbose=None)

            with temporary_tqdm_replacement():
                model = whisper.load_model(model)
                result = model.transcribe(self.file_path, language='en', fp16=False, verbose=None)


            srt_filepath = './bin/' + self.file_path.split('/')[-1][:-3] + 'srt'
            MakingSrt.write_srt(result, srt_filepath)

            from src.subtitles.handle_video import HandleVideo
            HandleVideo.handle_video(
            self.file_path.split("/")[-1], 
            self.file_path, 
            self.directory_path, 
            self.translate_var.get()
        )

            print("HandleVideo process completed!!!")

            # except Exception as e:
            #     print(f"An error has occurred: {e}")

            # else:
            #     self.clear_bin_directory('./bin')
                

        else:
            print("You must select the file and directory to continue processing.")


if __name__ == "__main__":
    # if os.path.exists('./bin') and os.path.isdir('./bin'):
    #     shutil.rmtree('./bin')
    root = tk.Tk()
    app = FileSelectorApp(root)
    print('You must not choose file.mp4 which has path with spaces.\nExample: "/home/user/auto-subs-desctop/videos/test.mp4" - correct path,\n"/home/user/auto subs desktop/videos/test test.mp4" - wrong path\n')
    print('If an error was received while the program was running, it is recommended to restart the application and start processing again\n')
    root.mainloop()


