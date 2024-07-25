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
        print('Progress of transcription process: ', int(((self._current * 100) / self.total)), '%')


class _CustomProgressBarForHandleVideo(_CustomProgressBar):

    def update(self, n):
        super().update(n)
        self._current += n

        # print("Progress: " + str(self._current) + "/" + str(self.total))
        print('Progress of handling video: ', int(((self._current * 100) / self.total)), '%')
  