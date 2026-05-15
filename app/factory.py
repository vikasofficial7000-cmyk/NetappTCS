"""Main application factory."""

from flask import Flask
from flask_cors import CORS
from app.config import config
from app.database.db_config import init_db
from app.utils.logger import setup_logging
from app.schedulers.task_scheduler import scheduler
from app.api.supply_chain_routes import supply_chain_bp
from app.api.disruption_routes import disruption_bp
from app.api.alert_routes import alert_bp


def create_app(config_name='development'):
    """Create and configure Flask application.

    Args:
        config_name: Configuration name (development, testing, production)

    Returns:
        Flask application instance
    """
    # Setup logging
    setup_logging()

    # Create app instance
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app)

    # Initialize database
    init_db(app)

    # Initialize scheduler
    scheduler.init_app(app)

    # Register blueprints
    app.register_blueprint(supply_chain_bp)
    app.register_blueprint(disruption_bp)
    app.register_blueprint(alert_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy'}, 200

    # Welcome endpoint
    @app.route('/', methods=['GET'])
    def welcome():
        return {
            'application': 'NetApp TCS - Supply Chain Disruption Notifier',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'supply_chains': '/api/supply-chains',
                'disruptions': '/api/disruptions',
                'alerts': '/api/alerts',
                'health': '/health'
            }
        }, 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500

    # Start scheduler
    with app.app_context():
        scheduler.start()

    return app
