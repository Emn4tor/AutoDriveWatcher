from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import os
import psutil
import pathlib
from datetime import datetime

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
CORS(app)  # Enable CORS for all routes


def get_file_info(path):
    try:
        stats = os.stat(path)
        return {
            'name': os.path.basename(path),
            'path': path,
            'type': 'folder' if os.path.isdir(path) else os.path.splitext(path)[1][1:] or 'file',
            'size': stats.st_size if os.path.isfile(path) else 0,
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat()
        }
    except Exception as e:
        print(f"Error getting file info for {path}: {e}")
        return None


@app.route('/')
def index():
    return render_template('streamR.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/api/drives')
def get_drives():
    drives = []
    for partition in psutil.disk_partitions():
        if partition.mountpoint:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                drives.append({
                    'name': f"Drive {partition.device}",
                    'path': partition.mountpoint,
                    'total': usage.total,
                    'free': usage.free
                })
            except Exception as e:
                print(f"Error getting drive info for {partition.mountpoint}: {e}")
    return jsonify(drives)


@app.route('/api/files')
def get_files():
    path = request.args.get('path', '')
    if not path:
        return jsonify([])

    try:
        items = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            file_info = get_file_info(full_path)
            if file_info:
                items.append(file_info)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search')
def search_files():
    term = request.args.get('term', '').lower()
    path = request.args.get('path', '')

    if not term or not path:
        return jsonify([])

    results = []
    try:
        for root, dirs, files in os.walk(path):
            for item in dirs + files:
                if term in item.lower():
                    full_path = os.path.join(root, item)
                    file_info = get_file_info(full_path)
                    if file_info:
                        results.append(file_info)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)