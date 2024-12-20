import os
from flask import Flask, send_from_directory
from routes import api
from config import Config

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    app.register_blueprint(api, url_prefix='/')

    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../frontend', path)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
