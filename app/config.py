"""Application configuration management."""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///netapp_tcs.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('DATABASE_ECHO', False)

    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    JSON_SORT_KEYS = False

    # Celery
    CELERY_BROKER_URL = os.getenv(
        'CELERY_BROKER_URL',
        'redis://localhost:6379/0'
    )
    CELERY_RESULT_BACKEND = os.getenv(
        'CELERY_RESULT_BACKEND',
        'redis://localhost:6379/0'
    )

    # Notifications
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    NOTIFICATION_FROM_EMAIL = os.getenv('NOTIFICATION_FROM_EMAIL')

    # Thresholds
    DISRUPTION_RISK_THRESHOLD = float(
        os.getenv('DISRUPTION_RISK_THRESHOLD', 7.0)
    )
    CRITICAL_ALERT_THRESHOLD = float(
        os.getenv('CRITICAL_ALERT_THRESHOLD', 8.5)
    )

    # Scheduler
    SCHEDULER_INTERVAL_MINUTES = 5


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
