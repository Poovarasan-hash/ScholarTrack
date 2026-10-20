import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from controllers.auth_controller import auth_bp

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

load_dotenv(BASE_DIR / ".env", override=True)


def create_app():
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path=""
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "scholartrack-super-secret-key-dev-2026")

    # Session cookie configuration
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production with HTTPS

    allowed_origins = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:5000,http://localhost:5000,null"
        ).split(",")
        if origin.strip()
    ]

    CORS(
        app,
        resources={
            r"/api/*": {"origins": allowed_origins}
        },
        supports_credentials=True
    )

    # Register API Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Serve Landing Page at root
    @app.route("/", methods=["GET"])
    def home():
        if (FRONTEND_DIR / "index.html").is_file():
            return send_from_directory(FRONTEND_DIR, "index.html")
        return jsonify({
            "success": True,
            "application": "ScholarTrack",
            "message": "Backend is running!",
            "version": "1.0.0"
        })

    # Serve static frontend pages & assets seamlessly
    @app.route("/<path:path>", methods=["GET"])
    def serve_frontend_files(path):
        target = FRONTEND_DIR / path
        if target.is_file():
            return send_from_directory(FRONTEND_DIR, path)
        if (FRONTEND_DIR / f"{path}.html").is_file():
            return send_from_directory(FRONTEND_DIR, f"{path}.html")
        if (FRONTEND_DIR / "index.html").is_file():
            return send_from_directory(FRONTEND_DIR, "index.html")
        return jsonify({"error": "Not found"}), 404

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "status": "healthy",
            "auth_endpoints": "/api/auth"
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=True
    )
