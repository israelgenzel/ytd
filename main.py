import os
import time
from google.colab import drive
import yt_dlp


# פונקציה להורדת הפלייליסט
def download_playlist(playlist_url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # אפשר לשנות לפי הצורך
        'outtmpl': '%(title)s.%(ext)s',  # מיקום שמירת הקבצים
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])



download_plylist("https://www.youtube.com/watch?v=_4c-YlGvt0k")
