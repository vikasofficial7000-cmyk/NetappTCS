"""Supply Chain API routes."""

from flask import Blueprint, request, jsonify
from app.services.supply_chain_service import SupplyChainService
from app.models.supply_chain import SupplyChainEntity
from app.utils.validators import validate_input
from loguru import logger

supply_chain_bp = Blueprint('supply_chain', __name__, url_prefix='/api/supply-chains')


@supply_chain_bp.route('', methods=['POST'])
def create_supply_chain():
    """Create a new supply chain entity."""
    try:
        is_valid, data, error = validate_input(request.json, SupplyChainEntity)
        if not is_valid:
            return {'error': error}, 400

        supply_chain = SupplyChainService.create_supply_chain(data)
        return {'id': supply_chain.id, 'message': 'Supply chain created successfully'}, 201
    except Exception as e:
        logger.error(f"Error creating supply chain: {str(e)}")
        return {'error': str(e)}, 500


@supply_chain_bp.route('/<int:chain_id>', methods=['GET'])
def get_supply_chain(chain_id):
    """Get supply chain by ID."""
    try:
        supply_chain = SupplyChainService.get_supply_chain(chain_id)
        if not supply_chain:
            return {'error': 'Supply chain not found'}, 404
        return supply_chain.to_dict(), 200
    except Exception as e:
        logger.error(f"Error retrieving supply chain: {str(e)}")
        return {'error': str(e)}, 500


@supply_chain_bp.route('', methods=['GET'])
def list_supply_chains():
    """List all supply chains with optional filters."""
    try:
        entity_type = request.args.get('entity_type')
        is_active = request.args.get('is_active')

        if is_active is not None:
            is_active = is_active.lower() == 'true'

        supply_chains = SupplyChainService.get_all_supply_chains(entity_type, is_active)
        return {
            'count': len(supply_chains),
            'data': [sc.to_dict() for sc in supply_chains]
        }, 200
    except Exception as e:
        logger.error(f"Error listing supply chains: {str(e)}")
        return {'error': str(e)}, 500


@supply_chain_bp.route('/<int:chain_id>', methods=['PUT'])
def update_supply_chain(chain_id):
    """Update supply chain entity."""
    try:
        is_valid, data, error = validate_input(request.json, SupplyChainEntity)
        if not is_valid:
            return {'error': error}, 400

        supply_chain = SupplyChainService.update_supply_chain(chain_id, data)
        if not supply_chain:
            return {'error': 'Supply chain not found'}, 404

        return {'message': 'Supply chain updated successfully'}, 200
    except Exception as e:
        logger.error(f"Error updating supply chain: {str(e)}")
        return {'error': str(e)}, 500
