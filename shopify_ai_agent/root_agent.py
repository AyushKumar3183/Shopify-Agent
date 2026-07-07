"""Root orchestrator agent for the eCommerce support workflow."""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.utils.context_utils import Aclosing
from google.genai import types
from typing_extensions import override

from agents.escalation import escalation_agent
from agents.intent import intent_agent
from agents.priority import priority_agent
from agents.reply import reply_agent
from constants import FINAL_RESPONSE_KEY, ROOT_AGENT_NAME
from state_utils import build_final_response

logger = logging.getLogger(__name__)


class SupportRootAgent(BaseAgent):
    """Orchestrates specialist agents and builds the final response in code.

    The root agent does not classify intents, write customer replies, or use an
    LLM for aggregation. It runs sub-agents sequentially, maintains session
    state, and deterministically constructs the final JSON payload.
    """

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Run specialist agents in order, then emit the aggregated response."""
        if not self.sub_agents:
            raise ValueError("support_root_agent requires specialist sub-agents.")

        for sub_agent in self.sub_agents:
            logger.info("Delegating to sub-agent: %s", sub_agent.name)
            async with Aclosing(sub_agent.run_async(ctx)) as agent_events:
                async for event in agent_events:
                    yield event
                    if ctx.should_pause_invocation(event):
                        logger.warning(
                            "Workflow paused at sub-agent: %s", sub_agent.name
                        )
                        return

        final_response = build_final_response(ctx.session.state)
        final_payload = final_response.model_dump()

        logger.info(
            "Workflow complete. intent=%s priority=%s escalate=%s",
            final_response.intent,
            final_response.priority,
            final_response.escalate,
        )

        yield Event(
            author=self.name,
            content=types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text=final_response.model_dump_json()
                    )
                ],
            ),
            state={FINAL_RESPONSE_KEY: final_payload},
        )


support_root_agent = SupportRootAgent(
    name=ROOT_AGENT_NAME,
    description=(
        "Root eCommerce support orchestrator. Runs intent, priority, reply, "
        "and escalation specialists sequentially, then returns structured JSON."
    ),
    sub_agents=[
        intent_agent,
        priority_agent,
        reply_agent,
        escalation_agent,
    ],
)

# Entry-point alias used by the FastAPI Runner.
root_agent = support_root_agent
