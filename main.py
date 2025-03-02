from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/download', methods=['GET'])
def download_video():
    
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        ydl_opts = {
            'format': 'bestvideo/best',  # אפשר לשנות לפי הצורך
            'outtmpl': 'temp',  # מיקום שמירת הקבצים
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # # מציאת הקובץ שהורד
        # downloaded_files = os.listdir()
        # if not downloaded_files:
        #     return jsonify({"error": "Download failed"}), 500

        filename = "download/temp"
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


