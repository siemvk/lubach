import os
import tempfile
from typing import Any, cast

from flask import Flask, request, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
	return response


@app.route('/health', methods=['GET', 'OPTIONS'])
def index():
	# Respond to CORS preflight
	if request.method == 'OPTIONS':
		return "", 200
	return "OK"

@app.route("/download/<id>/<begin>/<end>", methods=['GET', 'OPTIONS'])
def download(id, begin, end):
	if request.method == 'OPTIONS':
		return "", 200

	video_url = f"https://www.youtube.com/watch?v={id}"
	temp_dir = tempfile.mkdtemp(prefix="yt-dlp-")
	raw_output_template = os.path.join(temp_dir, "clip.%(ext)s")
	clip_path = os.path.join(temp_dir, "clip.mp4")

	ydl_opts: dict = {
		'format': 'bestvideo+bestaudio/best',
		'outtmpl': raw_output_template,
		'noplaylist': True,
		'quiet': True,
		'external_downloader': 'ffmpeg',
		'external_downloader_args': {
			'ffmpeg_i': ['-ss', begin, '-to', end],
		},
	}
	with YoutubeDL(cast(Any, ydl_opts)) as ydl:
		info = ydl.extract_info(video_url, download=True)
		file_path = ydl.prepare_filename(info)

	if not os.path.exists(file_path):
		base, _ = os.path.splitext(clip_path)
		for ext in ('.mp4', '.mkv', '.webm', '.m4a', '.mp3'):
			candidate = base + ext
			if os.path.exists(candidate):
				file_path = candidate
				break

	return send_file(file_path, as_attachment=True, download_name='clip.mp4')

@app.route("/audio/<id>/<begin>/<end>", methods=['GET', 'OPTIONS'])
def audio(id, begin, end):
	if request.method == 'OPTIONS':
		return "", 200

	video_url = f"https://www.youtube.com/watch?v={id}"
	temp_dir = tempfile.mkdtemp(prefix="yt-dlp-")
	raw_output_template = os.path.join(temp_dir, "clip.%(ext)s")
	clip_path = os.path.join(temp_dir, "clip.mp4")

	ydl_opts: dict = {
		'format': 'bestaudio/best',
		'outtmpl': raw_output_template,
		'noplaylist': True,
		'quiet': True,
		'external_downloader': 'ffmpeg',
		'external_downloader_args': {
			'ffmpeg_i': ['-ss', begin, '-to', end],
		},
	}
	with YoutubeDL(cast(Any, ydl_opts)) as ydl:
		info = ydl.extract_info(video_url, download=True)
		file_path = ydl.prepare_filename(info)

	if not os.path.exists(file_path):
		base, _ = os.path.splitext(clip_path)
		for ext in ('.mp4', '.mkv', '.webm', '.m4a', '.mp3'):
			candidate = base + ext
			if os.path.exists(candidate):
				file_path = candidate
				break

	return send_file(file_path, as_attachment=True, download_name='clip.mp4')


if __name__ == '__main__':
	# Bind to all interfaces on port 8080
	app.run(host='0.0.0.0', port=8080, debug=True)
