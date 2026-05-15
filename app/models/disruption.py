"""Disruption data model."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DisruptionData(BaseModel):
    """Disruption data schema."""

    id: Optional[int] = None
    supply_chain_id: int
    disruption_type: str = Field(..., description="Type of disruption (supply, demand, transport, etc.)")
    severity: float = Field(..., ge=0, le=10, description="Severity score 0-10")
    location: str
    description: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    affected_products: list[str] = Field(default_factory=list)
    estimated_impact_days: int = Field(default=0, ge=0)
    root_cause: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    status: str = Field(default="reported", description="Status: reported, investigating, mitigated, resolved")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "supply_chain_id": 1,
                "disruption_type": "transportation_delay",
                "severity": 7.5,
                "location": "Shanghai Port",
                "description": "Port congestion due to bad weather",
                "affected_products": ["Product A", "Product B"],
                "estimated_impact_days": 3
            }
        }
