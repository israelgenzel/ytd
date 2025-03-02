import requests
import os

# כתובת השרת שלך ב-Railway (עדכן בהתאם ל-URL שקיבלת)
RAILWAY_SERVER_URL = "https://ytd-production.up.railway.app/download"

def download_video(video_url):
    """שולח בקשת הורדה לשרת ושומר את הקובץ שהתקבל בשם הנכון"""

    params = {"url": video_url}
    response = requests.get(RAILWAY_SERVER_URL, params=params, stream=True)

    if response.status_code == 200:
        # קבלת שם הקובץ מהכותרות
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = "downloaded_video.mp4"

        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')

        # שמירת הקובץ
        save_path = os.path.join(os.getcwd(), filename)
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print(f"✅ הורדה הושלמה: {save_path}")
    else:
        print(f"❌ שגיאה: {response.json()}")

# דוגמה לשימוש
video_link = "https://www.youtube.com/watch?v=KxAuxNBY6SE"
download_video(video_link)
