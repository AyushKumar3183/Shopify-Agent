"""Shared constants for the Shopify support automation workflow."""

from typing import Final, Literal

# --- Model ---

GEMINI_MODEL: Final[str] = "gemini-2.5-flash"

# --- Intent labels ---

SHIPPING_DELAY: Final[str] = "Shipping Delay"
REFUND_REQUEST: Final[str] = "Refund Request"
RETURN_REQUEST: Final[str] = "Return Request"
PRODUCT_DAMAGE: Final[str] = "Product Damage"
CANCELLATION: Final[str] = "Cancellation"
GENERAL_INQUIRY: Final[str] = "General Inquiry"

SUPPORT_INTENTS: Final[tuple[str, ...]] = (
    SHIPPING_DELAY,
    REFUND_REQUEST,
    RETURN_REQUEST,
    PRODUCT_DAMAGE,
    CANCELLATION,
    GENERAL_INQUIRY,
)

IntentLabel = Literal[
    "Shipping Delay",
    "Refund Request",
    "Return Request",
    "Product Damage",
    "Cancellation",
    "General Inquiry",
]

# --- Priority labels ---

PRIORITY_HIGH: Final[str] = "High"
PRIORITY_MEDIUM: Final[str] = "Medium"
PRIORITY_LOW: Final[str] = "Low"

PRIORITY_LEVELS: Final[tuple[str, ...]] = (
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
)

PriorityLabel = Literal["High", "Medium", "Low"]

# --- Session state keys ---

INTENT_RESULT_KEY: Final[str] = "intent_result"
PRIORITY_RESULT_KEY: Final[str] = "priority_result"
REPLY_RESULT_KEY: Final[str] = "reply_result"
ESCALATION_RESULT_KEY: Final[str] = "escalation_result"
FINAL_RESPONSE_KEY: Final[str] = "final_response"

# --- Agent names ---

ROOT_AGENT_NAME: Final[str] = "support_root_agent"
