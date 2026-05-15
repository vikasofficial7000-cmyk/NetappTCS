"""Database configuration and initialization."""

from flask import Flask
from . import db


def init_db(app: Flask) -> None:
    """Initialize database.

    Args:
        app: Flask application instance
    """
    db.init_app(app)

    with app.app_context():
        db.create_all()


def reset_db(app: Flask) -> None:
    """Reset database (drop all tables).

    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
