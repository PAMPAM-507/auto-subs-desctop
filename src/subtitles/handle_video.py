import pysrt
import os
import sys

from .put_subs import PutSubs
from .my_translator import MyTranslator

class HandleVideo():

    # @staticmethod
    # def handle_video(name_of_video, path_for_video, path_for_new_video):
    #     mp4filename = name_of_video
    #     srtfilename = os.environ.get('PROJECT_ROOT') + \
    #         '/bin/' + (name_of_video)[0:-4] + '.srt'

    #     subtitles = pysrt.open(srtfilename)

    #     MyTranslator().make_translate(subtitles, name_of_video, srtfilename)
    #     PutSubs(mp4filename, srtfilename, path_for_video,
    #             path_for_new_video).generate_video_with_subtitles()

    @staticmethod
    def handle_video(name_of_video, path_for_video, path_for_new_video):
        while True:
            try:
                mp4filename = name_of_video
                srtfilename = os.environ.get('PROJECT_ROOT') + \
                    '/bin/' + (name_of_video)[0:-4] + '.srt'

                subtitles = pysrt.open(srtfilename)
                
                MyTranslator().make_translate(subtitles, name_of_video, srtfilename)
                PutSubs(mp4filename, srtfilename, path_for_video,
                        path_for_new_video).generate_video_with_subtitles()
                
            except Exception as e:
                print(e)
            
            else:
                break

