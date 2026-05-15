"""Supply chain service."""

from typing import Optional
from datetime import datetime
from loguru import logger
from app.database.models import SupplyChain
from app.database import db
from app.models.supply_chain import SupplyChainEntity


class SupplyChainService:
    """Service for handling supply chain operations."""

    @staticmethod
    def create_supply_chain(data: SupplyChainEntity) -> SupplyChain:
        """Create a new supply chain entity.

        Args:
            data: Supply chain entity data

        Returns:
            Created supply chain record
        """
        try:
            supply_chain = SupplyChain(
                name=data.name,
                entity_type=data.entity_type,
                location=data.location,
                contact_email=data.contact_email,
                contact_phone=data.contact_phone,
                products_handled=data.products_handled,
                risk_level=data.risk_level,
                is_active=data.is_active
            )
            db.session.add(supply_chain)
            db.session.commit()
            logger.info(f"Supply chain entity created with ID: {supply_chain.id}")
            return supply_chain
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating supply chain: {str(e)}")
            raise

    @staticmethod
    def get_supply_chain(chain_id: int) -> Optional[SupplyChain]:
        """Get supply chain by ID.

        Args:
            chain_id: Supply chain ID

        Returns:
            Supply chain record or None
        """
        return SupplyChain.query.get(chain_id)

    @staticmethod
    def get_all_supply_chains(entity_type: Optional[str] = None, is_active: Optional[bool] = None) -> list[SupplyChain]:
        """Get all supply chains with optional filters.

        Args:
            entity_type: Filter by entity type
            is_active: Filter by active status

        Returns:
            List of supply chains
        """
        query = SupplyChain.query
        if entity_type:
            query = query.filter_by(entity_type=entity_type)
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        return query.order_by(SupplyChain.created_at.desc()).all()

    @staticmethod
    def update_supply_chain(chain_id: int, data: SupplyChainEntity) -> Optional[SupplyChain]:
        """Update supply chain entity.

        Args:
            chain_id: Supply chain ID
            data: Updated supply chain data

        Returns:
            Updated supply chain record or None
        """
        try:
            supply_chain = SupplyChain.query.get(chain_id)
            if not supply_chain:
                return None

            supply_chain.name = data.name
            supply_chain.location = data.location
            supply_chain.contact_email = data.contact_email
            supply_chain.contact_phone = data.contact_phone
            supply_chain.products_handled = data.products_handled
            supply_chain.risk_level = data.risk_level
            supply_chain.is_active = data.is_active
            supply_chain.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Supply chain {chain_id} updated")
            return supply_chain
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating supply chain: {str(e)}")
            raise

    @staticmethod
    def update_health_check(chain_id: int) -> Optional[SupplyChain]:
        """Update supply chain health check timestamp.

        Args:
            chain_id: Supply chain ID

        Returns:
            Updated supply chain record or None
        """
        try:
            supply_chain = SupplyChain.query.get(chain_id)
            if not supply_chain:
                return None

            supply_chain.last_health_check = datetime.utcnow()
            db.session.commit()
            return supply_chain
        except Exception as e:
            logger.error(f"Error updating health check: {str(e)}")
            raise
