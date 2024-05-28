from typing import NoReturn
import pysrt
import os

from gtts import gTTS
from abc import ABC, abstractmethod
from moviepy.editor import VideoFileClip, CompositeAudioClip, AudioFileClip


class MakeAudioRecordABC(ABC):

    @staticmethod
    def check_directory(directory: str):
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file):
        if audio_clip.duration < duration:
            # print(f"Warning: Duration of audio file {audio_file} is shorter than the subtitle duration.")
            duration = audio_clip.duration

        return duration

    @staticmethod
    def text_to_speech(text, output_file):
        tts = gTTS(text=text, lang='ru')
        tts.save(output_file)

    @staticmethod
    def time_to_seconds(t):
        return t.hours * 3600 + t.minutes * 60 + t.seconds + t.milliseconds / 1000
    
    @staticmethod
    def close_audio_files(audio_clips):
        for audio_clip in audio_clips:
            audio_clip.close()


class MakeAudioRecord(MakeAudioRecordABC):

    def make_audio_for_each_subtitles(cls, subtitles: pysrt, path_of_audio: str) -> CompositeAudioClip:

        cls.check_directory(f'./{path_of_audio}/records')

        audio_clips = []

        for i, subtitle in enumerate(subtitles):
            start_time = cls.time_to_seconds(subtitle.start)
            end_time = cls.time_to_seconds(subtitle.end)
            duration = end_time - start_time
            text = subtitle.text

            audio_file = f"./{path_of_audio}/records/audio_{i}.mp3"
            cls.text_to_speech(text, audio_file)

            audio_clip = AudioFileClip(audio_file)

            duration = cls.check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file)
            
            audio_clip = audio_clip.set_start(start_time).set_duration(duration).volumex(2.0)
            audio_clips.append(audio_clip)

        return CompositeAudioClip(audio_clips), audio_clips

    def perform_audio_creation(cls, subtitles, path_of_audio: str) -> CompositeAudioClip:

        new_audio, audio_clips = cls.make_audio_for_each_subtitles(subtitles=subtitles, path_of_audio=path_of_audio)

        return new_audio, audio_clips