"""Intent agent for classifying eCommerce customer support messages."""

from google.adk.agents import Agent

from config import GEMINI_MODEL
from constants import INTENT_RESULT_KEY
from schemas import IntentOutput

from .prompt import INTENT_PROMPT

intent_agent = Agent(
    model=GEMINI_MODEL,
    name="intent_agent",
    description=(
        "Classifies eCommerce customer messages into support intents such as "
        "shipping delays, refunds, returns, product damage, cancellations, "
        "or general inquiries."
    ),
    instruction=INTENT_PROMPT,
    output_schema=IntentOutput,
    output_key=INTENT_RESULT_KEY,
)
