"""Application entry point using Gunicorn (for production)."""

import os
from app.factory import create_app

config_name = os.getenv('FLASK_ENV', 'production')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
