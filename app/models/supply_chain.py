"""Supply Chain Entity model."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SupplyChainEntity(BaseModel):
    """Supply Chain Entity schema."""

    id: Optional[int] = None
    name: str
    entity_type: str = Field(..., description="Type: supplier, warehouse, distributor, retailer")
    location: str
    contact_email: str
    contact_phone: Optional[str] = None
    products_handled: list[str] = Field(default_factory=list)
    risk_level: float = Field(default=0, ge=0, le=10)
    last_health_check: Optional[datetime] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Shanghai Distribution Center",
                "entity_type": "warehouse",
                "location": "Shanghai, China",
                "contact_email": "manager@warehouse.com",
                "products_handled": ["Product A", "Product B", "Product C"],
                "risk_level": 5.5
            }
        }
