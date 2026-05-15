"""Alert model."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Alert status."""

    PENDING = "pending"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Alert(BaseModel):
    """Alert schema."""

    id: Optional[int] = None
    disruption_id: int
    severity: AlertSeverity
    title: str
    message: str
    recipients: list[str]
    channels: list[str] = Field(default=["email", "dashboard"])
    status: AlertStatus = Field(default=AlertStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "disruption_id": 1,
                "severity": "high",
                "title": "Supply Disruption Alert",
                "message": "Major supply chain disruption detected in Shanghai Port",
                "recipients": ["manager@company.com"],
                "channels": ["email", "dashboard"]
            }
        }
