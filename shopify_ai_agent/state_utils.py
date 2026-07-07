"""Helpers for reading ADK session state and building the final API response."""

from __future__ import annotations

import json
import logging
from typing import Any, Mapping

from constants import (
    ESCALATION_RESULT_KEY,
    FINAL_RESPONSE_KEY,
    INTENT_RESULT_KEY,
    PRIORITY_RESULT_KEY,
    REPLY_RESULT_KEY,
)
from schemas import SupportResponse

logger = logging.getLogger(__name__)


def coerce_state_value(value: Any) -> dict[str, Any]:
    """Normalize ADK session state values into a dictionary."""
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            logger.debug("Could not parse session state value as JSON.")
    return {}


def build_final_response(state: Mapping[str, Any]) -> SupportResponse:
    """Deterministically merge specialist outputs into the final API response."""
    intent_data = coerce_state_value(state.get(INTENT_RESULT_KEY))
    priority_data = coerce_state_value(state.get(PRIORITY_RESULT_KEY))
    reply_data = coerce_state_value(state.get(REPLY_RESULT_KEY))
    escalation_data = coerce_state_value(state.get(ESCALATION_RESULT_KEY))

    missing_keys = [
        key
        for key, data in (
            (INTENT_RESULT_KEY, intent_data),
            (PRIORITY_RESULT_KEY, priority_data),
            (REPLY_RESULT_KEY, reply_data),
            (ESCALATION_RESULT_KEY, escalation_data),
        )
        if not data
    ]
    if missing_keys:
        raise ValueError(
            f"Support workflow missing required state keys: {', '.join(missing_keys)}"
        )

    response = SupportResponse(
        intent=intent_data["intent"],
        priority=priority_data["priority"],
        reply=reply_data["reply"],
        escalate=bool(escalation_data["escalate"]),
    )
    logger.info(
        "Built final response for intent=%s priority=%s escalate=%s",
        response.intent,
        response.priority,
        response.escalate,
    )
    return response


def extract_support_response(state: Mapping[str, Any]) -> SupportResponse:
    """Return the cached final response or build it from specialist state."""
    final_payload = coerce_state_value(state.get(FINAL_RESPONSE_KEY))
    if final_payload:
        return SupportResponse.model_validate(final_payload)
    return build_final_response(state)
