def sanitize_filename(filename):
    """ מנקה את שם הקובץ לפני השמירה """
    filename = filename.strip()  # הסרת רווחים מיותרים
    filename = re.sub(r'[\/:*?"<>|]', '', filename)  # הסרת תווים אסורים
    return filename

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

        # ניקוי שם הקובץ
        filename = sanitize_filename(filename)
        clean_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # שינוי שם הקובץ
        os.rename(filename, clean_path)

        if not os.path.exists(clean_path):
            return jsonify({"error": "Download failed"}), 500

        return send_file(clean_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
