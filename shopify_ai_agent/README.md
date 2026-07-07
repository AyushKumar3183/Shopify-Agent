# Shopify AI Support Automation

Google ADK multi-agent prototype for eCommerce customer support. A customer message flows through specialist agents (intent, priority, reply, escalation) and returns a structured JSON response.

**Architecture documentation:** [docs/architecture.md](docs/architecture.md)

## Architecture

```text
Customer Message
       ↓
POST /support (FastAPI)
       ↓
support_root_agent (orchestrator)
       ↓
Intent → Priority → Reply → Escalation
       ↓
build_final_response() (deterministic)
       ↓
Final JSON Response
```

## Tech Stack

- Google ADK (`Agent`, `BaseAgent`, `Runner`)
- Gemini 2.5 Flash
- FastAPI
- Python 3.11+
- Pydantic
- python-dotenv

## Project Structure

```text
shopify_ai_agent/
├── agents/
│   ├── intent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   ├── priority/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   ├── reply/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   ├── escalation/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   └── __init__.py
├── root_agent.py
├── schemas.py
├── constants.py
├── state_utils.py
├── config.py
├── main.py
├── requirements.txt
├── README.md
└── .env
```

## Setup

1. Create and activate a virtual environment:

```bash
cd shopify_ai_agent
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Gemini API key to `.env`:

```bash
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=False
```

## Run

From the `shopify_ai_agent` directory:

```bash
uvicorn main:app --reload
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/support" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My order has not arrived in 12 days and I want a refund."
  }'
```

Expected response shape:

```json
{
  "intent": "Refund Request",
  "priority": "High",
  "reply": "We apologize for the delay. Our support team is reviewing your refund request.",
  "escalate": true
}
```

## Agent Responsibilities

| Agent | Role |
|-------|------|
| **Root Agent** | Entry point; runs specialist sub-agents in order and aggregates output |
| **Intent Agent** | Classifies issue type (shipping, refund, return, damage, cancellation, inquiry) |
| **Priority Agent** | Assigns High / Medium / Low urgency |
| **Reply Agent** | Generates a concise professional response |
| **Escalation Agent** | Decides if a human should review the ticket |

## Notes

- Specialist agents use `output_schema` and `output_key` so results flow through ADK session state.
- The root agent orchestrates specialists sequentially and aggregates output in `state_utils.build_final_response()`.
- Set `GEMINI_MODEL` in `.env` to override the default `gemini-2.5-flash`.
