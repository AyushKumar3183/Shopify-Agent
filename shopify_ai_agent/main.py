"""FastAPI service for the Shopify/eCommerce support automation prototype."""

from __future__ import annotations

from dotenv import load_dotenv

# Load .env before ADK / agent imports so GOOGLE_API_KEY is available.
load_dotenv()

import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from config import APP_NAME
from root_agent import root_agent
from schemas import SupportRequest, SupportResponse
from state_utils import extract_support_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize shared resources when the API starts."""
    logger.info("Shopify support automation service started.")
    yield
    logger.info("Shopify support automation service stopped.")


app = FastAPI(
    title="Shopify AI Support Automation",
    description=(
        "Google ADK multi-agent prototype for eCommerce customer support."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


async def _run_support_workflow(message: str) -> SupportResponse:
    """Execute the root ADK orchestrator for a customer message."""
    user_id = "api_user"
    session_id = str(uuid.uuid4())

    logger.info("Starting support workflow session_id=%s", session_id)

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    response: SupportResponse | None = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text:
                try:
                    response = SupportResponse.model_validate_json(text)
                except ValueError:
                    logger.debug(
                        "Final event was not valid SupportResponse JSON."
                    )

    if response is not None:
        logger.info(
            "Workflow finished from final event session_id=%s",
            session_id,
        )
        return response

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        raise RuntimeError("Support session was not found after workflow execution.")

    return extract_support_response(session.state)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health endpoint for uptime checks."""
    return {"status": "ok"}


@app.post("/support", response_model=SupportResponse)
async def process_support_request(request: SupportRequest) -> SupportResponse:
    """Run the multi-agent support workflow for a customer message."""
    logger.info("Received support request message_length=%d", len(request.message))
    try:
        return await _run_support_workflow(request.message)
    except ValueError as exc:
        logger.error("Workflow validation error: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Support workflow failed.")
        raise HTTPException(
            status_code=500,
            detail="Support workflow failed. Check logs and API credentials.",
        ) from exc
