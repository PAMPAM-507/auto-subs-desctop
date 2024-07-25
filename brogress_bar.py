import os
import sys
import tqdm
import urllib.request 

class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n  # Set the initial value
        
    def update(self, n):
        super().update(n)
        self._current += n
        
        # Handle progress here
        print("Progress of transcription process: " + str(self._current) + "/" + str(self.total))

# Inject into tqdm.tqdm of Whisper, so we can see progress
import whisper.transcribe 
transcribe_module = sys.modules['whisper.transcribe']
transcribe_module.tqdm.tqdm = _CustomProgressBar

import whisper
model = whisper.load_model("tiny")

result = model.transcribe("./videos/test3.mp4", language="en", fp16=False, verbose=None)
print(result['text'])