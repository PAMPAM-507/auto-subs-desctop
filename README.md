# program automatic makes subtitles for video in many languages

First you need to install imagemagick, ffmpeg, python 3.11. 

Before install requirements it is better to make python virtualenv.

for windows
```
py -3.11 -m venv venv;
pip install -r requirements_for_windows.txt;
```

for linux
```
python3.11 -m venv venv;
pip3 install -r requirements.txt;
```

After installing requirements you need to to choose file.mp4 which you want to translate and directory where you want to save your new video with subtitles. Then choose size of model for recognize audio which you want. After that you need to press button 'execute'. Then the program should start work.
![Alt text](./images/image.png)
![Alt text](./images/image2.png)
