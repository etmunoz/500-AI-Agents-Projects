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

## Paso 2 — Higiene · 2026-09-11

### Lo que se buscó y no apareció

**No hay secretos, ni en el árbol trackeado ni en el historial completo.** Se escaneó `git log --all -p` contra los patrones de OpenAI, GitHub (clásico y fine-grained), AWS, Google, Slack y bloques de clave privada PEM. La única coincidencia es `sk-abc123fakekeynotreal0000000000`, declarada explícitamente como fixture falsa en el agente 21. **No hay nada que rotar.**

Los 24 `.env.example` traen solo marcadores (`your_openai_api_key_here` y equivalentes). Ningún `.env` real existió jamás en el historial. Cero artefactos generados versionados: sin `dist/`, sin `node_modules/`, sin `__pycache__`, sin `.sqlite`.

`images/star-history.svg` **sí** es un archivo generado y versionado, pero a propósito: lo produce y commitea el workflow `star-history.yml`, que para eso tiene `contents: write`. No se ignora.

`scripts/star-history.mjs` tiene consumidor real —dos invocaciones en ese mismo workflow—, así que no es un script huérfano. No queda nada anotado para el paso 7 por este motivo.

### Lo que se instaló

**`.gitignore`** — no existía ninguno. Patrones anclados a rutas exactas: `/web/node_modules/` en vez de `node_modules/` suelto, y las cinco salidas de agentes por su ruta completa (`/agents/04-sql-query-agent/demo.sqlite` y compañía) en vez de `*.csv` o `*.sqlite` globales, que esconderían contenido real.

Decisión deliberada de **no** ignorar `test_*.py`, que es lo que genera el agente 15 en su carpeta: el patrón escondería las pruebas reales el día que el repositorio tenga alguna. Excluir de más se ve idéntico a estar bien configurado, y es el riesgo que este paso advierte.

**Hooks** en `.githooks/`, con `core.hooksPath` apuntando ahí: `pre-commit` (secretos) y `pre-push` (comprobaciones), más `.githooks/comprobaciones` con los comandos reales de este proyecto.

**`scripts/revisar_secretos.py`** — el segundo motor del hook, en una de las rutas donde `pre-commit` lo busca por convención.

### Verificación — ejecutando, no leyendo

| Qué se probó | Resultado |
|---|---|
| Hook contra un secreto **inventado** (no uno de ejemplo de proveedor) | 🔴 **Frenó el commit** — `leaks found: 2`, HEAD sin moverse |
| Hook contra archivos limpios | 🟢 Pasó, y avisó que `revisor-local` no corrió |
| `git ls-files -i -c` — ¿algún archivo ya versionado quedó ignorado? | Ninguno |
| Clon limpio vs. árbol trackeado | Idénticos: 148 archivos, los 24 `.env.example` presentes |
| `pre-push` → markdown | 🟢 0 — 26 archivos, 0 hallazgos |
| `pre-push` → agentes (sintaxis) | 🟡 **2 = NO SÉ** — no hay Python en esta máquina |
| `pre-push` → web (build) | 🟡 **2 = NO SÉ** — falta `npm install` en `web/` |

> El clon limpio verificó el estado commiteado, que todavía no incluye el `.gitignore`. La conclusión se sostiene igual porque `git ls-files -i -c` ya probó que ningún archivo versionado queda excluido por los patrones nuevos.

### Lo que queda abierto

1. **Un solo motor de secretos activo.** `gitleaks` corre (Docker 28.5.1 con el demonio arriba); `revisar_secretos.py` **no**, porque en esta máquina Python es solo el alias de la Microsoft Store — está en el PATH y falla al ejecutarse, que es exactamente el falso positivo contra el que el hook se blinda probando el intérprete con `-c ""`. Si Docker está apagado, `pre-commit` responde "no sé" y **deja pasar**. Al instalar Python: `git config --local ingenieria.python <ruta>`.
2. **`core.hooksPath` es configuración local**, vive en `.git/config` y no se versiona. Cada clon nuevo tiene que correr `git config core.hooksPath .githooks` o queda sin protección. Hay que documentarlo en el paso 3 (reglas) y en el paso 5 (README).
3. ~~No hay `.gitattributes`.~~ **Resuelto** — el PM lo aprobó y entró en el mismo commit del paso 2. Motivo: `core.autocrlf` está en `true` **a nivel sistema** en Git para Windows, y sin `.gitattributes` cada clon decide solo el fin de línea. Ya se notaba: `scripts/star-history.mjs` llega al árbol de trabajo con CRLF. Lo grave no era el ruido en los diffs sino `.githooks/*`: un hook con CRLF falla con `bad interpreter` en Linux y macOS, y el repositorio queda **sin protección de secretos sin que nada lo avise**. MSYS lo tolera, que es peor — en Windows parece que funciona. Por eso los scripts POSIX llevan `eol=lf` explícito. Verificado que `git add --renormalize .` no cambia ni un archivo existente: los 145 de texto ya estaban en LF.
4. **Efecto colateral que conviene registrar:** con el `.gitignore` puesto, la afirmación de `SECURITY.md:36` —"`.env` files are gitignored by default"— **pasa a ser cierta**. La mitad documental del hallazgo 1 queda resuelta. Lo que sigue mal en ese archivo es el destinatario del reporte de seguridad, que apunta al upstream: paso 8.

---

## Paso 3 — Reglas de desarrollo · 2026-09-11

Producido: [`docs/reglas/reglas_desarrollo.md`](reglas/reglas_desarrollo.md) — 13 secciones más 4 bloques de anexo.

### Donde la plantilla y el proyecto se contradecían

Cuatro choques. En tres ganó el proyecto, y el motivo quedó escrito al lado: una convención distinta con motivo no es una brecha.

| # | Choque | Resolución | Motivo |
|---|---|---|---|
| 1 | §4.1 exige un encabezado de **siete campos** en todo archivo de código | **Gana el proyecto** | Verificado: **0 de 21** `agent.py` lo tienen; todos abren con docstring de módulo. Cada `agent.py` existe para leerse de corrido como ejemplo, y siete líneas de metadatos de proceso antes de la primera línea de enseñanza le restan a lo que el archivo hace. La trazabilidad ya está en `metadata.yaml` y en git. |
| 2 | §2.1 exige **un solo manifiesto** de dependencias | **Gana el proyecto** | Hay 25 `requirements.txt` por diseño. Un agente tiene que poder copiarse entero fuera del repositorio y funcionar — es lo que el proyecto vende, y está declarado en `agents/README.md`. Un manifiesto raíz además obligaría a resolver conflictos entre `crewai==0.80.0` y `langchain==0.3.0` que nunca conviven en el mismo entorno. |
| 3 | El anexo **B (base de datos relacional)** | **Bloque borrado entero** | El diagnóstico marcó el rasgo por el SQLite del agente 04, pero al mirarlo es una base de demo que el agente crea al vuelo y abre en modo solo-lectura (`?mode=ro&uri=true`). Nada de lo que el bloque exige —migraciones versionadas y reversibles, repositorios, cadena de conexión por variable de entorno, UTC— tiene dónde aplicarse. Dejarlo sería una regla que enseña a saltear las que sí. **Corrige el rasgo que este mismo informe había registrado de más.** |
| 4 | §10.4 pide un **registro único de requerimientos** | **Declarado innecesario**, no pendiente | Lo que el repositorio recibe son aportes de agentes, no requerimientos. El contrato de cada aporte es el README del agente más los cinco archivos obligatorios. Se escribió así en vez de dejar una marca 🚧 que nadie iba a llenar. |

### Bloques condicionales conservados y borrados

- **Conservados:** A (interfaz web), E (componentes con LLM), F (fuentes externas), I (librería/CLI), y los inline de *material didáctico*, *sin usuarios ni autenticación*, *datos personales* y *los documentos son el producto*.
- **Borrados:** B (ver arriba), C (contenedores), D (máquina compartida), G (portado), H (escritorio), y los inline de *múltiples usuarios o roles* y *más de una suite*.

### Dos mediciones nuevas que el diagnóstico no tenía

1. **`web/src/App.jsx` tiene 1.057 líneas** — por encima del umbral de 1.000 que el estándar marca como deuda técnica activa. Es además el archivo donde una interfaz acumula copias divergentes sin que nadie lo decida. Declarado en §4.4 y en el bloque A; partirlo no es trabajo de la adopción.
2. **Sólo 4 de los 21 agentes validan la salida del modelo** (Pydantic, `with_structured_output` o `json.loads` con manejo de error). Los otros 17 la consumen tal cual. Declarado como deuda en el bloque E, y como criterio para lo que entre de ahora en adelante.

También se verificó y se escribió como **propiedad a mantener**, no como observación: ningún `agent.py` usa `exec`, `eval`, `subprocess`, `os.system`, `PythonREPL` ni `shell=True`.

### Verificación

| Qué | Resultado |
|---|---|
| Huecos `<ASÍ>` sin rellenar | Ninguno |
| Enlaces relativos del documento | 6 de 6 resuelven |
| `AGENTS.md` apunta a las reglas con la ruta correcta | Sí — se le quitó la marca 🚧, que ya no aplicaba |
| `npx markdownlint-cli2` | 26 archivos, 0 hallazgos |

### Candidato a subir al manual central (se propone en el paso 9)

La trampa del **bit de ejecución de los hooks**: `core.filemode=false` en Git para Windows hace que un `chmod +x` no llegue al índice, y git **omite en silencio** un hook no ejecutable en Linux y macOS. Es la misma forma que la trampa del CRLF —una diferencia de plataforma que en Windows parece funcionar— y le pasaría a cualquier proyecto que instale los hooks desde Windows siguiendo el paso 2 tal como está escrito hoy. El paso 2 no lo menciona.

---

## Secuencia de adopción

- [x] 0. Diagnóstico — 2026-09-11
- [x] 1. `/ingenieria:puntero` — 2026-09-11 · `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`)
- [x] 2. `/ingenieria:higiene` — 2026-09-11 · `.gitignore`, `.gitattributes`, `.githooks/`, `scripts/revisar_secretos.py`
- [x] 3. `/ingenieria:reglas` — 2026-09-11 · `docs/reglas/reglas_desarrollo.md`
- [ ] 4. `/ingenieria:estructura`
- [ ] 5. `/ingenieria:readme-proyecto`
- [ ] 6. `/ingenieria:manuales`
- [ ] 7. `/ingenieria:auditoria`
- [ ] 8. `/ingenieria:seguridad`
- [ ] 9. `/ingenieria:cierre`
