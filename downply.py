import re
import requests
import os

import urllib

# כתובת השרת שלך ב-Railway (עדכן בהתאם ל-URL שקיבלת)
RAILWAY_SERVER_URL = "https://ytd-production.up.railway.app/download"
LOCAL_SERVER_URL = "http://127.0.0.1:8080/download"

def download_video(video_url):
    """שולח בקשת הורדה לשרת ושומר את הקובץ שהתקבל בשם הנכון"""

    params = {"url": video_url}
    response = requests.get(LOCAL_SERVER_URL, params=params, stream=True)

    if response.status_code == 200:
        # קבלת שם הקובץ מהכותרות
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = "downloaded_video.mp4"

       # חיפוש filename*=UTF-8 (עדיף כי הוא תומך בעברית)
        match_utf8 = re.search(r'filename\*=UTF-8\'\'([^";]+)', content_disposition)

        # אם לא נמצא filename*=UTF-8, ננסה למצוא filename=
        match_simple = re.search(r'filename="([^"]+)"', content_disposition)

        if match_utf8:
            filename = urllib.parse.unquote(match_utf8.group(1))  # פענוח שם הקובץ אם הוא מקודד
        elif match_simple and not match_simple.group(1).strip().startswith("-"):  
            # קח את filename= רק אם הוא לא שם ריק או מוזר
            filename = match_simple.group(1).strip()

        print("Filename:", filename)

        # שמירת הקובץ
        save_path = os.path.join(os.getcwd(), filename)
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print(f"✅ הורדה הושלמה: {save_path}")
    else:
        print(f"❌ שגיאה: {response.text}")

# דוגמה לשימוש
video_link = "https://www.youtube.com/watch?v=KxAuxNBY6SE"
download_video(video_link)
