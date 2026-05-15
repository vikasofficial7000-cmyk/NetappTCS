"""SQLAlchemy ORM models."""

from datetime import datetime
from . import db


class SupplyChain(db.Model):
    """Supply Chain Entity ORM model."""

    __tablename__ = 'supply_chains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)  # supplier, warehouse, distributor
    location = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(20))
    products_handled = db.Column(db.JSON, default=[])
    risk_level = db.Column(db.Float, default=0.0)
    last_health_check = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    disruptions = db.relationship('Disruption', backref='supply_chain', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'entity_type': self.entity_type,
            'location': self.location,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'products_handled': self.products_handled,
            'risk_level': self.risk_level,
            'last_health_check': self.last_health_check,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Disruption(db.Model):
    """Disruption ORM model."""

    __tablename__ = 'disruptions'

    id = db.Column(db.Integer, primary_key=True)
    supply_chain_id = db.Column(db.Integer, db.ForeignKey('supply_chains.id'), nullable=False)
    disruption_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    affected_products = db.Column(db.JSON, default=[])
    estimated_impact_days = db.Column(db.Integer, default=0)
    root_cause = db.Column(db.Text)
    mitigation_strategy = db.Column(db.Text)
    status = db.Column(db.String(50), default='reported')
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    alerts = db.relationship('AlertLog', backref='disruption', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'supply_chain_id': self.supply_chain_id,
            'disruption_type': self.disruption_type,
            'severity': self.severity,
            'location': self.location,
            'description': self.description,
            'affected_products': self.affected_products,
            'estimated_impact_days': self.estimated_impact_days,
            'root_cause': self.root_cause,
            'mitigation_strategy': self.mitigation_strategy,
            'status': self.status,
            'detected_at': self.detected_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class AlertLog(db.Model):
    """Alert Log ORM model."""

    __tablename__ = 'alert_logs'

    id = db.Column(db.Integer, primary_key=True)
    disruption_id = db.Column(db.Integer, db.ForeignKey('disruptions.id'), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.JSON, default=[])
    channels = db.Column(db.JSON, default=['email', 'dashboard'])
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    acknowledged_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'disruption_id': self.disruption_id,
            'severity': self.severity,
            'title': self.title,
            'message': self.message,
            'recipients': self.recipients,
            'channels': self.channels,
            'status': self.status,
            'created_at': self.created_at,
            'sent_at': self.sent_at,
            'acknowledged_at': self.acknowledged_at
        }
