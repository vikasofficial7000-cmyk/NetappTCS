"""Alert API routes."""

from flask import Blueprint, request, jsonify
from app.services.alert_service import AlertService
from app.models.alert import Alert
from app.utils.validators import validate_input
from loguru import logger

alert_bp = Blueprint('alert', __name__, url_prefix='/api/alerts')


@alert_bp.route('', methods=['POST'])
def create_alert():
    """Create a new alert."""
    try:
        is_valid, data, error = validate_input(request.json, Alert)
        if not is_valid:
            return {'error': error}, 400

        alert = AlertService.create_alert(data)
        return {
            'id': alert.id,
            'message': 'Alert created successfully'
        }, 201
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        return {'error': str(e)}, 500


@alert_bp.route('/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get alert by ID."""
    try:
        alert = AlertService.get_alert(alert_id)
        if not alert:
            return {'error': 'Alert not found'}, 404
        return alert.to_dict(), 200
    except Exception as e:
        logger.error(f"Error retrieving alert: {str(e)}")
        return {'error': str(e)}, 500


@alert_bp.route('/<int:alert_id>/send', methods=['POST'])
def send_alert(alert_id):
    """Send an alert."""
    try:
        success = AlertService.send_alert(alert_id)
        if not success:
            return {'error': 'Failed to send alert'}, 400
        return {'message': 'Alert sent successfully'}, 200
    except Exception as e:
        logger.error(f"Error sending alert: {str(e)}")
        return {'error': str(e)}, 500


@alert_bp.route('/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert."""
    try:
        alert = AlertService.acknowledge_alert(alert_id)
        if not alert:
            return {'error': 'Alert not found'}, 404
        return {'message': 'Alert acknowledged successfully'}, 200
    except Exception as e:
        logger.error(f"Error acknowledging alert: {str(e)}")
        return {'error': str(e)}, 500
