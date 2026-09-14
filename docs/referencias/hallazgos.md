# Hallazgos

> Generado por `scripts/referencias_cruzadas.py` (análisis estático). No editar a mano.



## ref_rota (1) — destino sugerido: **documentar**

> El documento apunta a algo que no existe: se renombro, se movio, o nunca se construyo? Un manual que promete lo que no hay es peor que uno incompleto.

| Objeto | Confianza | Detalle |
|---|---|---|
| `README.md` | alta | README.md tiene un link roto: `.github/workflows/star-history.yml` |

## funcion_muerta (9) — destino sugerido: **revisar**

> 1) Hay una superficie que deberia usarla? 2) Algun manual o test la menciona como si funcionara? 3) Existe su espejo CLI/interfaz? Recien si las tres dan que no: por que se escribio y que la dejo sin uso.

| Objeto | Confianza | Detalle |
|---|---|---|
| `crewai_mcp_course/lesson_02/agent.py::TextFormatterTool._run` | posible | Funcion definida y nunca llamada: TextFormatterTool._run |
| `crewai_mcp_course/lesson_02/agent.py::WordCountTool._run` | posible | Funcion definida y nunca llamada: WordCountTool._run |
| `crewai_mcp_course/lesson_03/agent.py::DateTimeTool._run` | posible | Funcion definida y nunca llamada: DateTimeTool._run |
| `crewai_mcp_course/lesson_03/agent.py::JsonFormatterTool._run` | posible | Funcion definida y nunca llamada: JsonFormatterTool._run |
| `crewai_mcp_course/lesson_03/agent.py::TaskPrioritizerTool._run` | posible | Funcion definida y nunca llamada: TaskPrioritizerTool._run |
| `crewai_mcp_course/lesson_03/mcp_server.py::calculate_project_metrics` | posible | Funcion definida y nunca llamada: calculate_project_metrics |
| `crewai_mcp_course/lesson_03/mcp_server.py::format_as_json` | posible | Funcion definida y nunca llamada: format_as_json |
| `crewai_mcp_course/lesson_03/mcp_server.py::get_datetime` | posible | Funcion definida y nunca llamada: get_datetime |
| `crewai_mcp_course/lesson_03/mcp_server.py::prioritize_tasks` | posible | Funcion definida y nunca llamada: prioritize_tasks |