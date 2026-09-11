# PDF Q&A Agent

Loads any PDF and lets you ask questions about it. Supports both single-question and interactive chat modes.

**Framework**: LlamaIndex  
**LLM**: GPT-4o-mini  

## Setup

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
# Interactive Q&A (recommended)
uv run python agent.py --pdf your_document.pdf

# Single question
uv run python agent.py --pdf research_paper.pdf --question "What methodology was used?"
```

## Use cases

- Research paper analysis
- Contract review
- Financial report Q&A
- Technical documentation chat
