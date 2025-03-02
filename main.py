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
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # וידוא שהקובץ קיים
        if not os.path.exists(filename):
            return jsonify({"error": "Download failed"}), 500

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
