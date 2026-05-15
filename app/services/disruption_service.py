"""Disruption detection service."""

from datetime import datetime
from typing import Optional
from loguru import logger
from app.database.models import Disruption, SupplyChain
from app.database import db
from app.models.disruption import DisruptionData


class DisruptionService:
    """Service for handling disruption operations."""

    @staticmethod
    def create_disruption(data: DisruptionData) -> Disruption:
        """Create a new disruption record.

        Args:
            data: Disruption data

        Returns:
            Created disruption record
        """
        try:
            disruption = Disruption(
                supply_chain_id=data.supply_chain_id,
                disruption_type=data.disruption_type,
                severity=data.severity,
                location=data.location,
                description=data.description,
                affected_products=data.affected_products,
                estimated_impact_days=data.estimated_impact_days,
                root_cause=data.root_cause,
                mitigation_strategy=data.mitigation_strategy,
                status=data.status
            )
            db.session.add(disruption)
            db.session.commit()
            logger.info(f"Disruption created with ID: {disruption.id}")
            return disruption
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating disruption: {str(e)}")
            raise

    @staticmethod
    def get_disruption(disruption_id: int) -> Optional[Disruption]:
        """Get disruption by ID.

        Args:
            disruption_id: Disruption ID

        Returns:
            Disruption record or None
        """
        return Disruption.query.get(disruption_id)

    @staticmethod
    def get_all_disruptions(supply_chain_id: Optional[int] = None, status: Optional[str] = None) -> list[Disruption]:
        """Get all disruptions with optional filters.

        Args:
            supply_chain_id: Filter by supply chain
            status: Filter by status

        Returns:
            List of disruptions
        """
        query = Disruption.query
        if supply_chain_id:
            query = query.filter_by(supply_chain_id=supply_chain_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Disruption.created_at.desc()).all()

    @staticmethod
    def update_disruption(disruption_id: int, data: DisruptionData) -> Optional[Disruption]:
        """Update disruption record.

        Args:
            disruption_id: Disruption ID
            data: Updated disruption data

        Returns:
            Updated disruption record or None
        """
        try:
            disruption = Disruption.query.get(disruption_id)
            if not disruption:
                return None

            disruption.severity = data.severity
            disruption.status = data.status
            disruption.root_cause = data.root_cause
            disruption.mitigation_strategy = data.mitigation_strategy
            disruption.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Disruption {disruption_id} updated")
            return disruption
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating disruption: {str(e)}")
            raise
