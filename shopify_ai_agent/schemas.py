"""Pydantic schemas for API contracts and agent structured outputs."""

from pydantic import BaseModel, Field

from constants import IntentLabel, PriorityLabel


class SupportRequest(BaseModel):
    """Incoming customer support message."""

    message: str = Field(
        ...,
        min_length=1,
        description="Raw customer message to analyze and respond to.",
    )


class SupportResponse(BaseModel):
    """Final aggregated support workflow response."""

    intent: str = Field(description="Classified customer intent.")
    priority: PriorityLabel = Field(description="Ticket urgency level.")
    reply: str = Field(description="Professional customer-facing reply.")
    escalate: bool = Field(
        description="Whether a human agent should review this ticket."
    )


class IntentOutput(BaseModel):
    """Intent classification result."""

    intent: IntentLabel = Field(description="Classified customer issue intent.")


class PriorityOutput(BaseModel):
    """Priority assessment result."""

    priority: PriorityLabel = Field(description="Urgency of the customer issue.")


class ReplyOutput(BaseModel):
    """Generated customer reply."""

    reply: str = Field(
        description="Concise, professional customer support response."
    )


class EscalationOutput(BaseModel):
    """Escalation decision result."""

    escalate: bool = Field(
        description="True when a human agent should review the ticket."
    )
