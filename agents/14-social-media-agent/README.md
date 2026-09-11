# Social Media Content Agent

Generates platform-optimized social media content (Twitter/X, LinkedIn, Instagram) from any topic.

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
uv run python agent.py --topic "The future of remote work"
uv run python agent.py --topic "Product launch announcement" --brand "YourBrand" --platforms "twitter,linkedin"
```
