"""Tests for services."""

import pytest
from app.services.analyzer_service import AnalyzerService
from app.database.models import Disruption, SupplyChain
from app.database import db
from datetime import datetime


def test_calculate_risk_score(app, db_session):
    """Test risk score calculation."""
    with app.app_context():
        # Create test data
        supply_chain = SupplyChain(
            name='Test Chain',
            entity_type='supplier',
            location='Test Location',
            contact_email='test@example.com',
            risk_level=5.0
        )
        db.session.add(supply_chain)
        db.session.commit()

        disruption = Disruption(
            supply_chain_id=supply_chain.id,
            disruption_type='supply_delay',
            severity=7.0,
            location='Test Port',
            description='Test disruption',
            affected_products=['Product A', 'Product B'],
            estimated_impact_days=3
        )
        db.session.add(disruption)
        db.session.commit()

        # Calculate risk score
        risk_score = AnalyzerService.calculate_risk_score(disruption, supply_chain)
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 10


def test_assess_disruption(app, db_session):
    """Test disruption assessment."""
    with app.app_context():
        # Create test data
        supply_chain = SupplyChain(
            name='Test Chain',
            entity_type='supplier',
            location='Test Location',
            contact_email='test@example.com',
            risk_level=5.0
        )
        db.session.add(supply_chain)
        db.session.commit()

        disruption = Disruption(
            supply_chain_id=supply_chain.id,
            disruption_type='supply_delay',
            severity=7.5,
            location='Test Port',
            description='Test disruption',
            affected_products=['Product A'],
            estimated_impact_days=5
        )
        db.session.add(disruption)
        db.session.commit()

        # Assess disruption
        assessment = AnalyzerService.assess_disruption(disruption, supply_chain)
        assert 'risk_score' in assessment
        assert 'requires_alert' in assessment
        assert 'is_critical' in assessment
        assert 'severity_level' in assessment
        assert 'recommendation' in assessment
