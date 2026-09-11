# Módulos — imports y grafo de llamadas

> Generado por `scripts/referencias_cruzadas.py` (análisis estático). No editar a mano.



## `agents/01-web-research-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `search_web`, `synthesize_report`, `build_graph`, `main`

## `agents/02-code-review-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `review_code`, `main`

## `agents/03-pdf-qa-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `build_index`, `interactive_qa`, `single_question`, `main`

## `agents/04-sql-query-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `create_demo_database`, `sqlite_uri`, `build_agent`, `main`

## `agents/05-email-drafting-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `build_email_crew`, `main`

## `agents/06-news-summarizer-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (3):** `fetch_news`, `summarize_news`, `main`

## `agents/07-github-issue-triager/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `parse_json_response`, `triage_issue`, `fetch_github_issue`, `main`

## `agents/08-data-analysis-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `create_sample_data`, `main`

## `agents/09-resume-parser-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (5):** `parse_json_response`, `read_resume_text`, `parse_resume`, `score_fit`, `main`

## `agents/10-meeting-notes-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `parse_json_response`, `generate_meeting_notes`, `format_notes`, `main`

## `agents/11-stock-research-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `get_stock_data`, `analyze_stock`, `format_number`, `main`

## `agents/12-travel-planner-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `build_travel_crew`, `main`

## `agents/13-customer-support-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (7):** `retrieve_context`, `check_escalation`, `generate_response`, `route_after_escalation_check`, `build_graph`, `load_kb_texts`, `main`

## `agents/14-social-media-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `generate_social_content`, `main`

## `agents/15-unit-test-generator/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `generate_tests`, `main`

## `agents/16-documentation-writer/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `extract_structure`, `generate_readme`, `add_docstrings`, `main`

## `agents/17-recipe-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `parse_json_response`, `get_recipes`, `display_recipe`, `main`

## `agents/18-job-application-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `run_job_application_crew`, `main`

## `agents/19-competitive-analysis-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (5):** `identify_competitors`, `analyze_competitor`, `generate_report`, `build_graph`, `main`

## `agents/20-multi-agent-debate/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (6):** `DebateAgent.__init__`, `DebateAgent.make_argument`, `DebateJudge.__init__`, `DebateJudge.evaluate`, `run_debate`, `main`

## `agents/21-pii-sanitization-agent/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (2):** `sanitize`, `main`

## `crewai_mcp_course/lesson_01/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (0):** —

## `crewai_mcp_course/lesson_02/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (3):** `WordCountTool._run`, `TextFormatterTool._run`, `run_crew`

## `crewai_mcp_course/lesson_03/agent.py`

- **importa:** —
- **importado por:** —
- **funciones (4):** `DateTimeTool._run`, `JsonFormatterTool._run`, `TaskPrioritizerTool._run`, `run_mcp_workflow`

## `crewai_mcp_course/lesson_03/mcp_server.py`

- **importa:** —
- **importado por:** —
- **funciones (5):** `create_mcp_server`, `get_datetime`, `prioritize_tasks`, `format_as_json`, `calculate_project_metrics`

## `herramientas/comun/raiz.py`

- **importa:** —
- **importado por:** —
- **funciones (1):** `resolver_raiz`

## `herramientas/seguridad/revisar_secretos.py`

- **importa:** —
- **importado por:** —
- **funciones (7):** `_tiene_entropia`, `_git`, `revisar_ruta`, `revisar_linea`, `_archivos_indexados`, `_lineas_agregadas`, `main`