# Competitive Analysis Agent

LangGraph multi-step agent that identifies competitors, analyzes each one, and generates a strategic competitive report.

**Framework**: LangGraph  
**LLM**: GPT-4o-mini + GPT-4o  

## Setup

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uv run python agent.py --company "Notion" --industry "productivity software"
uv run python agent.py --company "Stripe" --industry "payment processing"
uv run python agent.py --company "Figma" --industry "design tools"
```

## Output

- 5 competitor analyses
- Executive summary
- Market gaps and opportunities
- 5 strategic recommendations
- Threat assessment by competitor
