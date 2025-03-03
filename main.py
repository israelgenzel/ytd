from flask import Flask, request, send_file, jsonify, after_this_request
import yt_dlp
import os
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/download', methods=['GET'])
def download_video():
    print("download_video")
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location':'/ffmpeg.exe',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # מציאת הקובץ שהורד
        downloaded_files = os.listdir(DOWNLOAD_FOLDER)
        print(downloaded_files)
        if not downloaded_files:
            return jsonify({"error": "Download failed"}), 500

        print(f"✅ הורדה הושלמה: {downloaded_files[0]}")
        filename = os.path.join(DOWNLOAD_FOLDER, downloaded_files[0])

        # מחיקת הקובץ אחרי שליחה
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(filename):
                    time.sleep(1)  # חכה שנייה לוודא שהשליחה הסתיימה
                    os.remove(filename)
                    print(f"🗑️ קובץ נמחק: {filename}")
            except Exception as e:
                print(f"⚠️ שגיאה במחיקה: {e}")
            return response

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
