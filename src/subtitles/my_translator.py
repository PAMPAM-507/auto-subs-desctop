from abc import ABC, abstractmethod
import os

from googletrans import Translator, constants
from pprint import pprint
import pysrt


class MYTranslatorABC(ABC):

    @abstractmethod
    def make_translate(self, subtitles):
        pass


class MyTranslator(MYTranslatorABC):

    def make_translate(self, subtitles, path_for_video, path_for_subs):
        lst = []
        for s in subtitles:
            lst.append(s)

        sentences = lst
        lst = []

        for j in range(len(sentences)):
            translation = Translator().translate(text=sentences[j].text, src='en', dest="ru")
            lst.append(translation.text)

        for i in range(len(subtitles)):
            if sentences[i].start == subtitles[i].start and sentences[i].end == subtitles[i].end:
                subtitles[i].text = lst[i]

        subtitles.save(path_for_subs)
