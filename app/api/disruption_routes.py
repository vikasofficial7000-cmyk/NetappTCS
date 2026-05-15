"""Disruption API routes."""

from flask import Blueprint, request, jsonify
from app.services.disruption_service import DisruptionService
from app.services.analyzer_service import AnalyzerService
from app.services.supply_chain_service import SupplyChainService
from app.models.disruption import DisruptionData
from app.utils.validators import validate_input
from loguru import logger

disruption_bp = Blueprint('disruption', __name__, url_prefix='/api/disruptions')


@disruption_bp.route('', methods=['POST'])
def create_disruption():
    """Create a new disruption report."""
    try:
        is_valid, data, error = validate_input(request.json, DisruptionData)
        if not is_valid:
            return {'error': error}, 400

        disruption = DisruptionService.create_disruption(data)
        return {
            'id': disruption.id,
            'message': 'Disruption created successfully'
        }, 201
    except Exception as e:
        logger.error(f"Error creating disruption: {str(e)}")
        return {'error': str(e)}, 500


@disruption_bp.route('/<int:disruption_id>', methods=['GET'])
def get_disruption(disruption_id):
    """Get disruption by ID."""
    try:
        disruption = DisruptionService.get_disruption(disruption_id)
        if not disruption:
            return {'error': 'Disruption not found'}, 404

        supply_chain = SupplyChainService.get_supply_chain(disruption.supply_chain_id)
        assessment = AnalyzerService.assess_disruption(disruption, supply_chain)

        return {
            'disruption': disruption.to_dict(),
            'assessment': assessment
        }, 200
    except Exception as e:
        logger.error(f"Error retrieving disruption: {str(e)}")
        return {'error': str(e)}, 500


@disruption_bp.route('', methods=['GET'])
def list_disruptions():
    """List all disruptions with optional filters."""
    try:
        supply_chain_id = request.args.get('supply_chain_id', type=int)
        status = request.args.get('status')

        disruptions = DisruptionService.get_all_disruptions(supply_chain_id, status)
        return {
            'count': len(disruptions),
            'data': [d.to_dict() for d in disruptions]
        }, 200
    except Exception as e:
        logger.error(f"Error listing disruptions: {str(e)}")
        return {'error': str(e)}, 500


@disruption_bp.route('/<int:disruption_id>', methods=['PUT'])
def update_disruption(disruption_id):
    """Update disruption record."""
    try:
        is_valid, data, error = validate_input(request.json, DisruptionData)
        if not is_valid:
            return {'error': error}, 400

        disruption = DisruptionService.update_disruption(disruption_id, data)
        if not disruption:
            return {'error': 'Disruption not found'}, 404

        return {'message': 'Disruption updated successfully'}, 200
    except Exception as e:
        logger.error(f"Error updating disruption: {str(e)}")
        return {'error': str(e)}, 500
