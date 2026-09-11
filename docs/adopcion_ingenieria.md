# Adopción del manual de ingeniería — 500-AI-Agents-Projects

**Diagnóstico:** 2026-09-11 09:43
**Rasgos del proyecto:** interfaz web · base de datos relacional (SQLite de muestra) · componentes con LLM · fuentes de datos externas · datos personales o regulados · librería/CLI · fork con original de referencia aguas arriba

No aplican: contenedores · multiusuario · máquina compartida · escritorio · sin aplicación desplegable.

> **Sobre el último**: el repositorio *sí* tiene una aplicación desplegable — `web/` es una SPA de React 18 + Vite 6 que el workflow `jekyll-gh-pages.yml` publica en GitHub Pages en cada push a `main`. Los pasos 6 (manuales) y 8 (seguridad) **aplican**, aunque acotados: el producto es un catálogo navegable más 21 agentes que se ejecutan en la máquina de quien los clona.

**Herramientas de auditoría del repositorio central:** no se corrieron. `referencias_cruzadas.py` escribe seis archivos en `docs/referencias/` y su calibración es trabajo del paso 7. Ninguna cifra de este informe proviene de ellas: todo se midió con `git ls-files`, `git config`, `grep` y lectura directa.

---

## Brecha medida

| Área | Estado | Evidencia |
|---|---|---|
| Puerta de entrada | falta | No existe `AGENTS.md` ni `CLAUDE.md` en la raíz. Nada lleva al manual central. |
| Reglas | falta | No existe `docs/reglas/` ni ningún documento de reglas. `CONTRIBUTION.md` (8.874 B) cubre formato de PR, plantillas y estilo de commits; no declara stack, arquitectura de módulos, proceso ni Definition of Done. |
| Documentación | parcial | 30 `.md` versionados: 4 en la raíz, 22 en `agents/`, 3 en `.github/`, 1 en `crewai_mcp_course/`. No existe `docs/`. Sin carpeta de históricos. Sin índice de documentación en el README. Cero salidas generadas versionadas (bien). |
| Manuales | falta | 0 de los 8 del núcleo: usuario, administrador, técnico, integración, despliegue, seguridad, riesgos, resolución de problemas. |
| Higiene | **bloquea** | Sin `.gitignore` en ningún nivel (`git ls-files \| grep -i gitignore` → vacío). `core.hooksPath` sin configurar. `.git/hooks/` solo trae los `.sample`. |
| Calidad y verificación | **bloquea** | 0 archivos de prueba entre 145 versionados. Ningún workflow ejecuta Python. 6 workflows en CI: `dco`, `markdown-lint`, `link-checker`, `stale`, `star-history`, `jekyll-gh-pages`. El único linter cubre `.md`. |
| Seguridad | parcial | `SECURITY.md` existe, pero apunta al repositorio original y afirma algo que es falso (ver hallazgo 1). Sin modelo de amenaza, sin registro de riesgos, sin declaración de qué puede disparar el modelo. |
| Hoja de ruta | falta | Ninguna mención de roadmap, "planned" o "coming soon" en los 30 `.md`. No hay planes cerrados de dónde inferirla. |

**Superficie de código medida:** 2.482 renglones repartidos en 21 `agent.py` + 4 archivos del curso. Sin `exec`, `eval`, `subprocess`, `os.system`, `PythonREPL` ni `shell=True` en ninguno. El agente 04 abre SQLite en modo solo-lectura por defecto (`?mode=ro&uri=true`). Endpoints externos invocados: `api.github.com`, `api.trustboost.dev`, `newsapi.org`.

---

## Hallazgos, por severidad

### Bloquean trabajo seguro

**1. No hay `.gitignore` — y `SECURITY.md` asegura que sí lo hay.**

`SECURITY.md:36` dice textualmente que los archivos `.env` "are gitignored by default". No existe ningún `.gitignore` en el repositorio. Mientras tanto hay 24 carpetas con `.env.example` (21 agentes + 3 lecciones) y tanto el README como `agents/README.md` instruyen `cp .env.example .env` como paso de arranque.

El resultado: el primer `git add .` de cualquier contribuyente sube su clave de OpenAI, Tavily o NewsAPI. Y la documentación no se limita a omitir la protección — afirma que existe, que es peor: quien la lea deja de revisar.

**2. Sin hooks instalados.**

`core.hooksPath` vacío y `.git/hooks/` con puros `.sample`. Nada intercepta el commit del hallazgo anterior antes de que salga.

**3. Cero pruebas.**

Ni un archivo de test entre los 145 versionados. Ningún workflow de CI ejecuta Python — el pipeline valida markdown, enlaces del README y el sign-off de los PR, pero nunca corre el código. Los 2.482 renglones de agentes no los verifica nada.

> El agente 15 se llama `unit-test-generator`, pero genera pruebas para código de terceros. No prueba este repositorio.

### Cuestan tiempo cada vez

**4. Es un fork y toda la documentación apunta al original.**

Nueve referencias a `ashishpatel26/500-AI-Agents-Projects`: los cuatro badges del encabezado, el `git clone` del Quick Start (`README.md:40`), el gráfico de estrellas, el enlace de "Report Issue", el advisory de seguridad y los `assignees` de las dos plantillas de issue. Dos consecuencias concretas: quien siga el Quick Start al pie de la letra clona el repositorio de otra persona, y quien reporte una vulnerabilidad la manda al correo de otra persona.

**5. El titular no coincide con el contenido.**

"500+ AI Agent Projects & Use Cases" contra lo que hay: ~95 entradas de catálogo por framework (AutoGen 42, CrewAI 24, LangGraph 20, Agno 19), 28 por industria, y 21 agentes ejecutables. Alrededor de 139 ítems reales.

**6. `web/` no está documentado en ninguna parte.**

Es lo único que el repositorio despliega, y no aparece en el README, ni en la guía de navegación, ni tiene README propio. `grep -rn 'web/' --include='*.md'` no devuelve una sola línea. Para saber que existe hay que leer el workflow de GitHub Pages.

### Deuda declarable

7. Ningún `.md` tiene encabezado con audiencia ni fecha de última revisión. 30 archivos sin forma de saber cuál se pudrió.
8. `link-checker.yml` solo revisa `README.md`. Los 22 README de `agents/` quedan fuera del chequeo de enlaces.
9. El agente 21 envía texto con PII a `https://api.trustboost.dev`, un tercero. Es su propósito declarado y está bien que exista, pero no figura en ningún modelo de amenaza porque no hay ninguno. Entra en el paso 8.
10. Sin hoja de ruta. No hay documento ni planes cerrados de los que extraerla; habrá que preguntársela al PM.
11. **Python no está instalado en esta máquina** (solo el alias del Microsoft Store). Hoy no se puede ejecutar ni verificar localmente nada de `agents/`. Es del entorno, no del repositorio, pero bloquea la verificación desde el paso 7.

---

## Lo que NO se va a tocar, y por qué

- **El alcance acotado de `.markdownlint-cli2.jsonc`.** Desactiva diez reglas cosméticas y limita los globs, con el motivo escrito en comentarios dentro del propio archivo ("reformatting 400 lines to satisfy a linter buys nothing"). Es una convención distinta con motivo declarado: se respeta.
- **Los agentes autocontenidos.** Sin `requirements.txt` en la raíz, sin monorepo, cada carpeta con sus dependencias. Es una decisión explícita de `agents/README.md` ("No monorepo setup needed") y sostiene el caso de uso del repositorio.
- **Relación con el upstream: decidida — el fork diverge.** El PM lo resolvió el 2026-09-11. Las nueve referencias a `ashishpatel26/500-AI-Agents-Projects` (badges, `git clone` del Quick Start, enlace de issues, gráfico de estrellas, advisory de seguridad y los `assignees` de las dos plantillas de issue) **se reescriben a `etmunoz/`**. Eso no es trabajo del paso 1: el README va en el paso 5 y el contacto de seguridad en el paso 8. Queda anotado acá para que no se pierda entre medio.

---

## Secuencia de adopción

- [x] 0. Diagnóstico — 2026-09-11
- [x] 1. `/ingenieria:puntero` — 2026-09-11 · `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`)
- [ ] 2. `/ingenieria:higiene`
- [ ] 3. `/ingenieria:reglas`
- [ ] 4. `/ingenieria:estructura`
- [ ] 5. `/ingenieria:readme-proyecto`
- [ ] 6. `/ingenieria:manuales`
- [ ] 7. `/ingenieria:auditoria`
- [ ] 8. `/ingenieria:seguridad`
- [ ] 9. `/ingenieria:cierre`
