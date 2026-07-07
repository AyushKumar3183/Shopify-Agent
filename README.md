# Shopify AI Support Automation

Google ADK multi-agent prototype for eCommerce customer support. A customer message flows through specialist agents (intent, priority, reply, escalation) and returns a structured JSON response.

**Full architecture documentation:** [shopify_ai_agent/docs/architecture.md](shopify_ai_agent/docs/architecture.md)

## Architecture

```text
Customer / API Client
       ↓
POST /support (FastAPI)
       ↓
ADK Runner (InMemorySessionService)
       ↓
SupportRootAgent (BaseAgent Orchestrator)
       ↓
Intent → Priority → Reply → Escalation
       ↓
build_final_response() (deterministic)
       ↓
SupportResponse (Pydantic Model)
       ↓
Customer / API Client
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
.
├── shopify_ai_agent/          # Application source code
│   ├── agents/
│   │   ├── intent/
│   │   ├── priority/
│   │   ├── reply/
│   │   └── escalation/
│   ├── docs/                  # Architecture diagrams & docs
│   ├── root_agent.py
│   ├── main.py
│   ├── schemas.py
│   ├── constants.py
│   ├── state_utils.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

## Setup

1. Clone the repository and enter the app directory:

```bash
git clone https://github.com/AyushKumar3183/Shopify-Agent.git
cd Shopify-Agent/shopify_ai_agent
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# Or from repo root: source ../venv/bin/activate if venv is one level up
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your Gemini API key:

```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY=your_key_here
```

## Run

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

Expected response:

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
| **SupportRootAgent** | Orchestrates specialists sequentially; deterministic aggregation |
| **Intent Agent** | Classifies issue type (shipping, refund, return, damage, cancellation, inquiry) |
| **Priority Agent** | Assigns High / Medium / Low urgency |
| **Reply Agent** | Generates a concise professional response |
| **Escalation Agent** | Decides if a human should review the ticket |

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](shopify_ai_agent/docs/architecture.md) | System design, layers, session state, sequence diagrams |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/support` | Run support workflow on a customer message |

## Notes

- Specialist agents use `output_schema` and `output_key` for ADK session state.
- Final response is built deterministically in `state_utils.build_final_response()` — no LLM aggregation.
- Model name is set in `constants.py` (`GEMINI_MODEL = "gemini-2.5-flash"`).
- Never commit `.env` — API keys are loaded from environment variables.
