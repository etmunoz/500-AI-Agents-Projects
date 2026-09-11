# Recipe Recommendation Agent

Suggests 3 recipes from your available ingredients with full instructions, nutritional info, and chef tips.

**Framework**: LangChain  
**LLM**: GPT-4o-mini  

## Setup

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uv run python agent.py --ingredients "chicken, garlic, lemon, rosemary"
uv run python agent.py --ingredients "tofu, broccoli, ginger, soy sauce" --diet vegan --time 20
uv run python agent.py --ingredients "pasta, tomatoes, basil, parmesan" --servings 4
```
