"""Escalation agent for deciding human handoff on support tickets."""

from google.adk.agents import Agent

from config import GEMINI_MODEL
from constants import ESCALATION_RESULT_KEY
from schemas import EscalationOutput

from .prompt import ESCALATION_PROMPT

escalation_agent = Agent(
    model=GEMINI_MODEL,
    name="escalation_agent",
    description=(
        "Decides whether a human support agent should review the ticket "
        "based on intent, priority, sentiment, and policy exceptions."
    ),
    instruction=ESCALATION_PROMPT,
    output_schema=EscalationOutput,
    output_key=ESCALATION_RESULT_KEY,
)
