"""Tests for supply chain endpoints."""

import pytest
import json


def test_create_supply_chain(client):
    """Test creating a supply chain."""
    data = {
        'name': 'Test Warehouse',
        'entity_type': 'warehouse',
        'location': 'Test City',
        'contact_email': 'test@example.com',
        'contact_phone': '1234567890',
        'products_handled': ['Product A', 'Product B'],
        'risk_level': 5.0
    }
    response = client.post(
        '/api/supply-chains',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_supply_chain(client):
    """Test retrieving a supply chain."""
    # First create a supply chain
    data = {
        'name': 'Test Warehouse',
        'entity_type': 'warehouse',
        'location': 'Test City',
        'contact_email': 'test@example.com',
        'products_handled': ['Product A'],
        'risk_level': 5.0
    }
    create_response = client.post(
        '/api/supply-chains',
        data=json.dumps(data),
        content_type='application/json'
    )
    chain_id = create_response.get_json()['id']

    # Then retrieve it
    get_response = client.get(f'/api/supply-chains/{chain_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['name'] == 'Test Warehouse'


def test_list_supply_chains(client):
    """Test listing supply chains."""
    response = client.get('/api/supply-chains')
    assert response.status_code == 200
    assert 'count' in response.get_json()
    assert 'data' in response.get_json()


def test_invalid_supply_chain(client):
    """Test creating supply chain with invalid data."""
    data = {
        'name': 'Test Warehouse'
        # Missing required fields
    }
    response = client.post(
        '/api/supply-chains',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.get_json()
