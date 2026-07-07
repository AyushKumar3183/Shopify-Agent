"""Reply agent for generating professional eCommerce support responses."""

from google.adk.agents import Agent

from config import GEMINI_MODEL
from constants import REPLY_RESULT_KEY
from schemas import ReplyOutput

from .prompt import REPLY_PROMPT

reply_agent = Agent(
    model=GEMINI_MODEL,
    name="reply_agent",
    description=(
        "Generates concise, professional customer support replies tailored "
        "to the classified intent and priority."
    ),
    instruction=REPLY_PROMPT,
    output_schema=ReplyOutput,
    output_key=REPLY_RESULT_KEY,
)
