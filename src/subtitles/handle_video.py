import pysrt
import os
import sys



from .put_subs import PutSubs
from .my_translator import MyGoogleTranslator, MyLocalTranslator

class HandleVideo():

    @staticmethod
    def handle_video(name_of_video, path_for_video, path_for_new_video):
        try:
            mp4filename = name_of_video
            srtfilename = os.environ.get('PROJECT_ROOT') + \
                '/bin/' + (name_of_video)[0:-4] + '.srt'

            subtitles = pysrt.open(srtfilename)
            
            # MyGoogleTranslator().make_translate(subtitles, srtfilename)
            MyLocalTranslator().make_translate(subtitles, srtfilename)
            PutSubs(mp4filename, srtfilename, path_for_video,
                    path_for_new_video).generate_video_with_subtitles()
            
        except Exception as e:
            print(e)
            

