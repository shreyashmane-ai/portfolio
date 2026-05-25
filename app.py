"""Application factory for the portfolio site.

Initializes Flask app with database-backed models and blueprint registration
for main, auth, and admin routes.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def _build_database_uri() -> str:
    """Construct SQLAlchemy database URI.

    Priority:
    1. PostgreSQL DATABASE_URL (Render production)
    2. MySQL local development
    3. SQLite fallback
    """

    # Render PostgreSQL
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Fix Render postgres URL format
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1
            )

        return database_url

    # Local MySQL
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")

    if db_user and db_password:
        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get("DB_PORT", "3306")
        db_name = os.environ.get("DB_NAME", "myportfolio")

        return (
            f"mysql+pymysql://{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}"
            f"?charset=utf8mb4"
        )

    # SQLite fallback
    base_dir = os.path.abspath(os.path.dirname(__file__))
    sqlite_path = os.path.join(base_dir, "data.db")

    return f"sqlite:///{sqlite_path}"
    

def create_app(config: dict | None = None) -> Flask:
    """Create and configure Flask application.
    
    Args:
        config: Optional dict to update app config
        
    Returns:
        Configured Flask app instance
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "thunder-dev-secret-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = _build_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Mail / SMTP configuration (optional)
    app.config["SMTP_HOST"] = os.environ.get("SMTP_HOST")
    app.config["SMTP_PORT"] = os.environ.get("SMTP_PORT")
    app.config["SMTP_USER"] = os.environ.get("SMTP_USER")
    app.config["SMTP_PASSWORD"] = os.environ.get("SMTP_PASSWORD")
    app.config["MAIL_FROM"] = os.environ.get("MAIL_FROM")
    app.config["MAIL_TO"] = os.environ.get("MAIL_TO")
    app.config["SMTP_USE_SSL"] = os.environ.get("SMTP_USE_SSL", "0") in ("1", "true", "True")

    if config:
        app.config.update(config)

    # Register extensions (lazy import to avoid circular imports)
    from modules.extensions import db, migrate, login_manager, csrf

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Wire user loader
    from modules.models import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        """Load user by ID for Flask-Login."""
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    # Register blueprints
    from modules.main.routes import bp as main_bp
    from modules.auth.routes import bp as auth_bp
    from modules.admin.routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    # app.run(debug=True, port=5000)
    app.run(host = '0.0.0.0', debug=True)
