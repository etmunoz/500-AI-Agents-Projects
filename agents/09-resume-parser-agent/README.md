# Resume Parser Agent

Parses resumes (TXT or PDF) into structured JSON and optionally scores candidate fit against a job description.

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
# Parse only (uses built-in sample resume)
uv run python agent.py

# Parse your resume
uv run python agent.py --resume path/to/resume.pdf

# Parse + fit score
uv run python agent.py --resume resume.pdf --job-desc "Senior Python Engineer with K8s experience..."
```

## Output includes

- Structured JSON: name, email, skills, experience, education
- Candidate summary
- Fit score (0-100) vs job description
- Hire/Consider/Pass recommendation
