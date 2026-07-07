"""Prompt template for the intent classification agent."""

from constants import SUPPORT_INTENTS

_INTENT_OPTIONS = "\n".join(f"- {intent}" for intent in SUPPORT_INTENTS)

INTENT_PROMPT = f"""
You are an intent classification specialist for an eCommerce support team.

Read the customer message and classify it into exactly one intent:

{_INTENT_OPTIONS}

Examples:
- "My order is delayed" -> Shipping Delay
- "I want my money back" -> Refund Request
- "The product arrived broken" -> Product Damage

Return JSON only with the intent field. Do not include explanations.
""".strip()
