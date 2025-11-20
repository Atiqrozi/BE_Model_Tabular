from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)  # biar bisa diakses dari frontend React/Next.js kalau perlu

    # contoh route sederhana
    @app.route("/")
    def home():
        return {"message": "API is running!"}

    from .routes import bp as predict_bp

    app.register_blueprint(predict_bp, url_prefix="/")

    return app
