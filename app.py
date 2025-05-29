from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        # yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'extract_flat': True,  # Extract metadata only
        }
        
        # Get video info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract relevant information
            video_info = {
                'title': info.get('title', ''),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': []
            }
            
            # Get available formats
            formats = info.get('formats', [])
            for f in formats:
                if f.get('url'):
                    video_info['formats'].append({
                        'format_id': f.get('format_id', ''),
                        'ext': f.get('ext', ''),
                        'resolution': f.get('resolution', ''),
                        'filesize': f.get('filesize', 0),
                        'url': f.get('url', '')
                    })
            
            return jsonify(video_info)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True) 