"""Application entry point."""

import os
from app.factory import create_app
from app.utils.logger import logger

# Create app instance
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    host = app.config.get('API_HOST', '0.0.0.0')
    port = app.config.get('API_PORT', 5000)
    debug = app.config.get('DEBUG', False)

    logger.info(f"Starting NetApp TCS Application on {host}:{port}")
    logger.info(f"Environment: {config_name}")
    logger.info(f"Debug Mode: {debug}")

    app.run(host=host, port=port, debug=debug)
