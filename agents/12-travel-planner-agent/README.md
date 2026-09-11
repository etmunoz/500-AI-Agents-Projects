# Travel Planner Agent

Three-agent CrewAI system that creates personalized travel itineraries with destination research, day-by-day plans, and budget breakdown.

**Framework**: CrewAI  
**LLM**: GPT-4o-mini  

## Setup

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uv run python agent.py --destination "Tokyo, Japan" --days 7 --budget 3000
uv run python agent.py --destination "Paris, France" --days 5 --budget 5000 --interests "art, wine, architecture"
```
