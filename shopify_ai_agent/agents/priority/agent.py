"""Priority agent for determining eCommerce support ticket urgency."""

from google.adk.agents import Agent

from config import GEMINI_MODEL
from constants import PRIORITY_RESULT_KEY
from schemas import PriorityOutput

from .prompt import PRIORITY_PROMPT

priority_agent = Agent(
    model=GEMINI_MODEL,
    name="priority_agent",
    description=(
        "Determines ticket urgency (High, Medium, Low) using eCommerce "
        "support rules and customer sentiment."
    ),
    instruction=PRIORITY_PROMPT,
    output_schema=PriorityOutput,
    output_key=PRIORITY_RESULT_KEY,
)
