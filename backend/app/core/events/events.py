from datetime import datetime, timezone
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base event payload structure."""

    event_id: UUID = Field(default_factory=uuid4)
    event_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class IncidentDetected(BaseEvent):
    """Triggered when an anomaly or alert signals an incident."""

    event_name: str = "IncidentDetected"
    incident_id: UUID
    service_name: str
    severity: str
    title: str


class InvestigationStarted(BaseEvent):
    """Triggered when the reasoning agent begins inspection."""

    event_name: str = "InvestigationStarted"
    incident_id: UUID
    agent_id: str


class RootCauseGenerated(BaseEvent):
    """Triggered when a root cause summary is completed."""

    event_name: str = "RootCauseGenerated"
    incident_id: UUID
    confidence_score: float
    root_cause_summary: str


class ReportCreated(BaseEvent):
    """Triggered when a postmortem or summary report is generated."""

    event_name: str = "ReportCreated"
    incident_id: UUID
    report_id: UUID


class NotificationSent(BaseEvent):
    """Triggered when message notifications are dispatched to Slack/Teams/PagerDuty."""

    event_name: str = "NotificationSent"
    channel: str
    recipient: str
    status: str
