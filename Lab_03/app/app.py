
# Student: mohamed nabil se3

from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

APP_VERSION = os.environ.get('APP_VERSION', '1.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Kubernetes!",
        "pod_name": socket.gethostname(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "healthy"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/info')
def info():
    return jsonify({
        "pod_name": socket.gethostname(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "python_version": os.popen("python --version").read().strip()
    })

if __name__ == '__main__':
    print(f"[APP] Starting on pod: {socket.gethostname()}")
    app.run(host='0.0.0.0', port=5000, debug=False)