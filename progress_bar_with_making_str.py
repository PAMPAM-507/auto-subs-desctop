import os
import sys
import tqdm
import whisper
import datetime

class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n

    def update(self, n):
        super().update(n)
        self._current += n

        # print("Progress: " + str(self._current) + "/" + str(self.total))
        print('Progress: ', int(((self._current * 100) / self.total)), '%')


import whisper.transcribe
transcribe_module = sys.modules['whisper.transcribe']
transcribe_module.tqdm.tqdm = _CustomProgressBar

model = whisper.load_model('tiny')
video_file = './videos/test3.mp4'
result = model.transcribe(video_file, language='en', fp16=False, verbose=None)

def convert_seconds(seconds):
    """Convert seconds to SRT time format."""
    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

def write_srt(transcription_result, srt_filepath):
    segments = transcription_result['segments']
    with open(srt_filepath, 'w', encoding='utf-8') as srt_file:
        for i, segment in enumerate(segments):
            start_time = convert_seconds(segment['start'])
            end_time = convert_seconds(segment['end'])
            text = segment['text'].strip()
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")

srt_filepath = video_file[:-3] + 'srt'

write_srt(result, srt_filepath)
print(f"Transcription saved to {srt_filepath}")
