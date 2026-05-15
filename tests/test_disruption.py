"""Tests for disruption endpoints."""

import pytest
import json
from datetime import datetime


def test_create_disruption(client):
    """Test creating a disruption."""
    # First create a supply chain
    sc_data = {
        'name': 'Test Warehouse',
        'entity_type': 'warehouse',
        'location': 'Test City',
        'contact_email': 'test@example.com',
        'products_handled': ['Product A'],
        'risk_level': 5.0
    }
    sc_response = client.post(
        '/api/supply-chains',
        data=json.dumps(sc_data),
        content_type='application/json'
    )
    chain_id = sc_response.get_json()['id']

    # Create disruption
    data = {
        'supply_chain_id': chain_id,
        'disruption_type': 'supply_delay',
        'severity': 7.5,
        'location': 'Test Port',
        'description': 'Test disruption',
        'affected_products': ['Product A'],
        'estimated_impact_days': 5
    }
    response = client.post(
        '/api/disruptions',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_disruption(client):
    """Test retrieving a disruption."""
    # Create supply chain and disruption
    sc_data = {
        'name': 'Test Warehouse',
        'entity_type': 'warehouse',
        'location': 'Test City',
        'contact_email': 'test@example.com',
        'products_handled': ['Product A'],
        'risk_level': 5.0
    }
    sc_response = client.post(
        '/api/supply-chains',
        data=json.dumps(sc_data),
        content_type='application/json'
    )
    chain_id = sc_response.get_json()['id']

    d_data = {
        'supply_chain_id': chain_id,
        'disruption_type': 'supply_delay',
        'severity': 7.5,
        'location': 'Test Port',
        'description': 'Test disruption',
        'affected_products': ['Product A'],
        'estimated_impact_days': 5
    }
    d_response = client.post(
        '/api/disruptions',
        data=json.dumps(d_data),
        content_type='application/json'
    )
    disruption_id = d_response.get_json()['id']

    # Get disruption
    get_response = client.get(f'/api/disruptions/{disruption_id}')
    assert get_response.status_code == 200
    response_data = get_response.get_json()
    assert 'disruption' in response_data
    assert 'assessment' in response_data


def test_list_disruptions(client):
    """Test listing disruptions."""
    response = client.get('/api/disruptions')
    assert response.status_code == 200
    assert 'count' in response.get_json()
    assert 'data' in response.get_json()
