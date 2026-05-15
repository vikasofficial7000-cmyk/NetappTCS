"""Tests for alert endpoints."""

import pytest
import json


def test_create_alert(client):
    """Test creating an alert."""
    # First create supply chain and disruption
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

    # Create alert
    alert_data = {
        'disruption_id': disruption_id,
        'severity': 'high',
        'title': 'Test Alert',
        'message': 'This is a test alert',
        'recipients': ['test@example.com'],
        'channels': ['email', 'dashboard']
    }
    response = client.post(
        '/api/alerts',
        data=json.dumps(alert_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_get_alert(client):
    """Test retrieving an alert."""
    # Setup: Create supply chain, disruption, and alert
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

    alert_data = {
        'disruption_id': disruption_id,
        'severity': 'high',
        'title': 'Test Alert',
        'message': 'This is a test alert',
        'recipients': ['test@example.com'],
        'channels': ['email']
    }
    a_response = client.post(
        '/api/alerts',
        data=json.dumps(alert_data),
        content_type='application/json'
    )
    alert_id = a_response.get_json()['id']

    # Get alert
    get_response = client.get(f'/api/alerts/{alert_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['title'] == 'Test Alert'
