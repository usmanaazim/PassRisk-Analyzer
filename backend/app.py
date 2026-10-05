"""Password Security Evaluation API. Passwords are never logged or stored."""

from __future__ import annotations

import logging

from flask import Flask, request
from flask_cors import CORS

from api.analysis_routes import analysis_bp
from api.health_routes import health_bp
from config import CORS_ORIGINS, DEBUG, HOST, PORT

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("passwordguard")


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().lower()
        if "password=" in message or "password:" in message or "password_a" in message:
            record.msg = "[redacted log line]"
            record.args = ()
        return True


logger.addFilter(RedactingFilter())


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, origins=CORS_ORIGINS, supports_credentials=False)
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(analysis_bp, url_prefix="/api")

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(404)
    def not_found(_error):
        return {"error": "Not found."}, 404

    @app.errorhandler(500)
    def server_error(_error):
        return {"error": "Internal server error."}, 500

    @app.before_request
    def reject_password_query_params():
        if "password" in request.args:
            return {"error": "Passwords must not be sent in the URL."}, 400
        return None

    return app


app = create_app()


if __name__ == "__main__":
    logger.info("Starting PasswordGuard API on %s:%s (debug=%s)", HOST, PORT, DEBUG)
    app.run(host=HOST, port=PORT, debug=DEBUG)
