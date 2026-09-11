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

**13 referencias al original, en 6 archivos.** Inventario línea por línea, medido el 2026-09-11 con `grep -rnE 'ashishpatel26|ashishpatel\.ce\.2011' --include='*.md' --include='*.yml'`:

| Archivo | Línea | Qué es |
|---|---|---|
| `README.md` | 5, 6, 7, 10 | Los cuatro badges del encabezado (stars, forks, contributors, last-commit) |
| `README.md` | 40 | El `git clone` del Quick Start |
| `README.md` | 300 | El enlace del gráfico de estrellas |
| `README.md` | 316 | El pie: "Report Issue" y "Request Agent" |
| `SECURITY.md` | 15 | Correo de contacto de seguridad |
| `SECURITY.md` | 16 | URL del advisory privado |
| `CODE_OF_CONDUCT.md` | 35 | Correo para denunciar conducta |
| `.github/ISSUE_TEMPLATE/bug_report.md` | 6 | `assignees` |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 6 | `assignees` |
| `.github/workflows/link-checker.yml` | 35 | Regla que **excluye** la URL del upstream del chequeo de enlaces |

Dos consecuencias concretas: quien siga el Quick Start al pie de la letra clona el repositorio de otra persona, y quien reporte una vulnerabilidad —o una conducta— la manda al correo de otra persona.

> **Corrección del 2026-09-11.** Este informe decía originalmente "nueve referencias en cuatro archivos". El conteo salió de un `grep` que sólo miraba `*.md` con el patrón `ashishpatel26`, y se le escaparon tres: el correo del mantenedor original en `SECURITY.md` y en `CODE_OF_CONDUCT.md` —que el patrón no cubría— y la regla de exclusión de `link-checker.yml`, que está en un `.yml`. La cifra corregida es 13 en 6 archivos, y cambia el alcance de los pasos 5 y 8.

**5. El titular no coincide con el contenido.**

"500+ AI Agent Projects & Use Cases" contra lo que hay: ~95 entradas de catálogo por framework (AutoGen 42, CrewAI 24, LangGraph 20, Agno 19), 28 por industria, y 21 agentes ejecutables. Alrededor de 139 ítems reales.

**6. `web/` no está documentado en ninguna parte.**

Es lo único que el repositorio despliega, y no aparece en el README, ni en la guía de navegación, ni tiene README propio. `grep -rn 'web/' --include='*.md'` no devuelve una sola línea. Para saber que existe hay que leer el workflow de GitHub Pages.

### Deuda declarable

7. Ningún `.md` tiene encabezado con audiencia ni fecha de última revisión. 30 archivos sin forma de saber cuál se pudrió.
8. `link-checker.yml` solo revisa `README.md`. Los 22 README de `agents/` quedan fuera del chequeo de enlaces.
9. El agente 21 envía texto con PII a `https://api.trustboost.dev`, un tercero. Es su propósito declarado y está bien que exista, pero no figura en ningún modelo de amenaza porque no hay ninguno. Entra en el paso 8.
10. Sin hoja de ruta. No hay documento ni planes cerrados de los que extraerla; habrá que preguntársela al PM.
11. ~~**Python no está instalado en esta máquina**~~ — **Resuelto el 2026-09-11 con `uv`.** Ver la sección *Entorno de Python* más abajo. Lo que el hallazgo no anticipaba: instalar Python **no alcanzó**, porque los alias de la Store siguen antes en el PATH. Hubo que declarar la ruta del intérprete.

---

## Lo que NO se va a tocar, y por qué

- **El alcance acotado de `.markdownlint-cli2.jsonc`.** Desactiva diez reglas cosméticas y limita los globs, con el motivo escrito en comentarios dentro del propio archivo ("reformatting 400 lines to satisfy a linter buys nothing"). Es una convención distinta con motivo declarado: se respeta.
- **Los agentes autocontenidos.** Sin `requirements.txt` en la raíz, sin monorepo, cada carpeta con sus dependencias. Es una decisión explícita de `agents/README.md` ("No monorepo setup needed") y sostiene el caso de uso del repositorio.
- **Relación con el upstream: decidida — el fork diverge.** El PM lo resolvió el 2026-09-11. Las **13 referencias** a `ashishpatel26` **se reescriben a `etmunoz/`** — el inventario línea por línea está en el hallazgo 4. Eso no es trabajo del paso 1: el `README.md` va en el paso 5, y `SECURITY.md`, `CODE_OF_CONDUCT.md`, las plantillas de issue y `link-checker.yml` en el paso 8. Queda anotado acá para que no se pierda entre medio.

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

## Paso 4 — Estructura documental · 2026-09-11

### Cero movimientos, y es un resultado válido

**No se ejecutó ni un solo `git mv`.** `docs/` tiene exactamente dos archivos —`adopcion_ingenieria.md` y `reglas/reglas_desarrollo.md`— y los creó esta misma adopción, en los pasos 0 y 3, ya en la ruta estándar. No hay nada fuera de lugar porque no hay nada más.

Tampoco había salidas generadas versionadas dentro de `docs/` (`find docs -type f ! -name '*.md'` → vacío), así que no hubo nada que sacar ni que agregar al `.gitignore`.

**No se crearon las carpetas vacías.** Una carpeta vacía no informa: promete un contenido que no existe, y quien la abra va a asumir que el proceso se abandonó.

### Las carpetas ausentes, declaradas

| Carpeta | Estado | Motivo, o el costo de no tenerla |
|---|---|---|
| `docs/requerimientos/` | **No aplica** | Lo que este repositorio recibe son aportes de agentes, no requerimientos. El contrato de cada aporte es el `README.md` del agente más los cinco archivos obligatorios. Declarado en §10.4 de las reglas. |
| `docs/planes/` y `planes/historicos/` | **No se usa todavía** | **El costo:** el trabajo que cabe en una sesión queda registrado en el mensaje de commit, y alcanza. El que abarque varias sesiones **se pierde**, porque el mensaje no se escribe hasta el final y la conversación no sobrevive. Se crea con el primer trabajo que no entre en una sesión. |
| `docs/revisiones/` y `revisiones/historicos/` | **No se usa todavía** | **El costo:** hoy no hay dónde dejar el resultado real de una validación, así que la evidencia vive en el cuerpo del commit y no se puede releer por tema. Se crea junto con `planes/`: un walkthrough sin plan que lo origine no tiene de qué informar. |
| `docs/manuales/` | **Pendiente** | 🚧 La crea el paso 6 (`/ingenieria:manuales`). |
| `docs/referencias/` | **Pendiente** | 🚧 La crea el paso 7 (`/ingenieria:auditoria`), que es donde se calibran las herramientas que la llenan. |
| `docs/reglas/` | ✅ Existe | Paso 3. |
| `docs/roadmap.md` | ✅ Creada en este paso | Ver abajo. |

`docs/adopcion_ingenieria.md` —este archivo— queda suelto en la raíz de `docs/` a propósito: es un documento **vivo** de estado, y la estructura estándar reserva ese lugar para ellos.

### La hoja de ruta, que no existía

Creada: [`docs/roadmap.md`](roadmap.md).

Se sembró **sólo con intenciones que ya estaban escritas** y vivían donde nadie las iba a releer. No hay planes cerrados ni walkthroughs de donde extraer, y el código no tiene una sola marca de intención: `grep -rnE 'TODO|FIXME|FUTURE|XXX|HACK'` sobre todos los `.py`, `.js`, `.jsx` y `.mjs` devuelve **cero**. El resultado se escribe aunque dé cero.

Lo que sí apareció, y de dónde salió:

| Entrada | Horizonte | De dónde salió |
|---|---|---|
| Cerrar la secuencia de adopción | Próximo | Trabajo en curso |
| Reescribir las 13 referencias al upstream | Próximo | Decisión del PM, 2026-09-11 |
| Las cinco categorías de aporte que `CONTRIBUTION.md` promete y no existen | Después | `CONTRIBUTION.md:14-18` — plantillas, integraciones, arneses de evaluación, experimentos reproducibles, utilidades de visualización. **Ninguna tiene hoy dónde vivir.** |
| Acercar el catálogo al número que promete el nombre | Después | El nombre del repositorio y el título del `README.md` contra las ~139 entradas reales |
| Un arnés que verifique que los agentes siguen corriendo | Algún día | Medición del paso 3: 20 de 21 agentes dependen de un proveedor externo y de una versión fijada de framework |

**Lo que deliberadamente NO entró a la hoja de ruta**, porque está roto y no es intención de futuro: las cero pruebas, las 1.057 líneas de `App.jsx`, los 17 agentes que no validan la salida del modelo, el verificador de enlaces que sólo mira `README.md`, y `web/` sin documentar. Todo eso vive como defecto medido en este mismo informe. Una hoja de ruta llena de defectos es un rastreador de errores con peores herramientas.

### Referencias corregidas

Ninguna por movimiento —no hubo movimientos—, pero **cuatro por un conteo mal medido**: ver la corrección del hallazgo 4. `AGENTS.md`, este informe (dos lugares) y las reglas (dos lugares) afirmaban "nueve referencias al upstream en cuatro archivos"; el número real es **13 en 6**. La trampa quedó registrada en §11.2 de las reglas, porque tiene mecanismo: todo inventario que vaya a un documento se escribe con el comando que lo produjo al lado, cubriendo todas las extensiones y todos los patrones del concepto.

No se corrió `referencias_cruzadas.py`: escribe en `docs/referencias/` y su calibración es trabajo del paso 7. Los enlaces se verificaron uno por uno con `test -e`.

---

## Paso 5 — README del proyecto · 2026-09-11

### Lo que se sacó por estar duplicado

**La sección "Contributing".** Tenía dos listas —"Ways to contribute" (4 ítems) y "To contribute" (4 pasos)— que son un resumen parcial de `CONTRIBUTION.md`, un archivo de 8.874 B con 18 secciones. Dos copias de lo mismo, y ninguna decía ser la copia: quien leía el README creía tener el panorama de cómo contribuir y tenía un extracto.

Ahora es una línea y un enlace, más las dos únicas cosas que alguien necesita saber **antes** de abrir el PR y que el README es el lugar natural para decir: que hace falta `Signed-off-by` o el CI rechaza, y dónde están las reglas que gobiernan el código.

> **Duplicación detectada pero NO tocada**, porque excede este paso: `CONTRIBUTION.md` tiene su propia sección *"Security, secrets & responsible disclosure"* (línea 168) que solapa con `SECURITY.md`, y una sección *"Code of Conduct"* (línea 202) que solapa con `CODE_OF_CONDUCT.md`. Es solapamiento entre manuales, que es trabajo del paso 6.

### Lo que se agregó, que no existía

| Sección | Por qué |
|---|---|
| **Status** | No había ninguna. Seis cifras, cada una con el comando que la produjo y la fecha. Incluye las dos incómodas: 0 pruebas y ~139 ítems contra el "500+" del título. |
| **Repository structure** | `web/` no aparecía en **ningún** `.md` del repositorio (hallazgo 6). Ahora está en el mapa, en el índice y en el Quick Start. |
| **Tests** | Dice que no hay ninguna, y agrega la tabla de qué mira cada workflow **y qué no**. Incluye que `link-checker` sólo cubre `README.md`. |
| **Scope & limits** | No existía. Siete límites explícitos, para que nada no mencionado se asuma funcionando. El más importante: los agentes **se ejecutan en tu máquina y gastan tu crédito**. |
| **Engineering conventions** | El enlace al manual central y el límite con las reglas propias. |

### El índice de documentación, ruteado por intención

La "Navigation Guide" era una tabla de 6 filas que sólo cubría el catálogo. Ahora son tres tablas —**usar**, **modificar**, **operar o auditar**— con 15 destinos, y una nota explícita de lo que todavía **no** está escrito (`docs/manuales/`, `docs/riesgos.md`) para que el índice no prometa lo que no existe.

### Las referencias al upstream

**7 de las 13 corregidas** — todas las del `README.md`: los 4 badges, el `git clone` del Quick Start, el gráfico de estrellas y el pie. `grep -nE 'ashishpatel' README.md` devuelve vacío.

Las 6 restantes están fuera del alcance de este paso y van al paso 8: `SECURITY.md` (2), `CODE_OF_CONDUCT.md` (1), las dos plantillas de issue (2) y `link-checker.yml` (1).

### Verificación

| Qué | Resultado |
|---|---|
| Enlaces relativos | **16 de 16** resuelven |
| Anclas internas (`#…`) | **7 de 7** resuelven — confirmado además por MD051, que está activo |
| `npx markdownlint-cli2` | 26 archivos, 0 hallazgos |
| Comandos del Quick Start | `git clone` y los dos `npm` **se corrieron**. El build: 1674 módulos en 2,07 s |
| Bloque `pip` / `python agent.py` | **No se re-corrió**: esta máquina no tiene Python. Está dicho en el propio README en vez de dejarlo pasar como verificado |

### Hallazgo nuevo: el despliegue no es reproducible

Al correr `npm install` apareció `web/package-lock.json`, que **no estaba versionado**. `jekyll-gh-pages.yml:41` usa `npm install` —no `npm ci`—, así que el despliegue no falla por la ausencia, pero **cada publicación a GitHub Pages resuelve las dependencias de cero**. Con `^` en `package.json` (`react: ^18.3.1`, `vite: ^6.0.1`), el sitio desplegado puede cambiar de versiones sin que ningún commit lo registre, y contradice §7.1 de las reglas: *todo artefacto derivado es regenerable desde su fuente*.

**No se versionó el lockfile en este paso**: es una decisión de reproducibilidad con consecuencias propias, no un arreglo de README. Queda para el paso 7 o para una decisión del PM antes.

---

## Paso 6 — Manuales · 2026-09-11

**El paso aplica.** El rasgo *sin aplicación desplegable* no corresponde: `web/` se publica a GitHub Pages y 21 agentes se ejecutan en máquinas ajenas. Pero aplica **acotado**: de los ocho del núcleo, dos se escribieron y seis no, cada uno con su motivo.

### Corrección de un hallazgo del paso 5

El paso 5 anotó que `CONTRIBUTION.md` duplicaba `SECURITY.md` y `CODE_OF_CONDUCT.md`. **Al leerlas, no las duplica:** son 3 y 2 líneas que remiten a los archivos dedicados sin restatear su contenido, que es exactamente lo que el estándar pide. Hallazgo retirado.

**La duplicación real estaba en `SECURITY.md`**, y era de la otra clase: un archivo contestando **dos preguntas de dos audiencias**.

### El mapeo contra el núcleo

| Manual | Contesta | Veredicto |
|---|---|---|
| `manual_usuario.md` | ¿Cómo hago mi trabajo con esto? | **Ya existe, distribuido** — son los 21 `README.md` de agente. Un archivo único sería una copia peor y divergiría. El hueco real no era el manual: era que **no había contrato** de qué debe contener cada uno (ver abajo). |
| `manual_administrador.md` | ¿Cómo lo configuro y opero día a día? | **No aplica.** No hay nada que administrar: sin servidor, sin cuentas, sin operación diaria. Lo único operativo —activar los hooks— está en el README y en las reglas §5. |
| `manual_tecnico.md` | ¿Cómo está construido y por qué así? | **Ya existe** — `reglas_desarrollo.md` §2 (stack), §3 (arquitectura de módulos) y §3.1 (decisiones tomadas con su fecha y motivo). Escribirlo aparte sería la séptima copia divergente. |
| `manual_integracion.md` | ¿Cómo hablo con él desde otro sistema? | **No aplica.** Nada expone una API, nada es importable, nada se publica en un registro de paquetes. |
| `manual_despliegue.md` | ¿Cómo lo pongo en producción desde cero? | ✅ **Escrito** |
| `manual_seguridad.md` | ¿Es seguro, y cómo se verifica? | 🚧 **Pendiente del paso 8**, que es quien lo escribe. No se inventa acá. |
| `manual_riesgos.md` | ¿Qué puede salir mal y qué sigue abierto? | 🚧 **Pendiente del paso 8.** |
| `manual_resolucion_problemas.md` | Algo falló, ¿qué hago? | ✅ **Escrito** |

Condicionales: `manual_agentes.md` queda cubierto por el anexo E de las reglas, y `manual_datos_personales.md` por el bloque §9 más lo que escriba el paso 8. `manual_espacio.md` y `manual_migracion.md` no aplican (sin máquina compartida, sin portado).

### Por qué dos y no ocho

Los dos que se escribieron tienen **contenido medido, no inventado**:

- **`manual_despliegue.md`** — nada documentaba que `web/` se publica a Pages, que un fork tiene que **habilitar Pages a mano** o el workflow falla recién en el último paso, que `concurrency: pages` encola en vez de pisar, que `base` está fijo al nombre del repositorio, ni que Vite hornea las `VITE_*` en tiempo de build.
- **`manual_resolucion_problemas.md`** — es el hueco que el estándar reporta ausente en cinco de siete proyectos. Acá tiene 16 entradas con síntoma, causa y qué hacer, **todas medidas durante esta adopción**: el alias de Python de la Store, los hooks sin activar, el CRLF, el `venv` equivocado, el sitio en blanco por el `base`.

Los otros seis no se escribieron. Un manual escrito para llenar una casilla es peor que su ausencia, porque además afirma.

### El archivo que se partió

`SECURITY.md` contestaba dos preguntas de dos audiencias: *"encontré una vulnerabilidad, ¿cómo la reporto?"* (investigador externo) y *"¿cómo escribo o corro un agente sin meter la pata?"* (colaborador). El segundo lector tenía que atravesar el primero para llegar a lo suyo.

La mitad de buenas prácticas se movió a `CONTRIBUTION.md`, dentro de su sección de seguridad, que es donde un colaborador la busca. `SECURITY.md` quedó con una sola pregunta y un enlace al otro lado. Los enlaces se redirigieron en el mismo commit.

Al moverlas se corrigieron dos afirmaciones: la de los `.env` "gitignored by default" ahora explica que el hook **sólo protege un clon donde fue activado**, y se agregó la propiedad de que ningún agente usa `exec`/`eval`/`subprocess` y que mantenerla requiere aprobación.

### El hueco que no era un manual

**Los 21 README de agente tienen 12 formas distintas.** 20 de 21 comparten `Setup` y `Run`; de ahí en adelante no hay acuerdo, y la misma sección aparece como `Output` (4 veces), `Sample Output` (2) y `Output includes` (2). El agente 21 no tiene ninguna de las dos.

Como estos README **son** el manual de usuario, la brecha no era un manual faltante sino la falta de contrato. Se escribió en `CONTRIBUTION.md`: seis secciones con nombres exactos —`Setup`, `Run`, `Output`, `Cost`, `Limits` más la introducción—, con `Cost` y `Limits` como novedad. **No se reescribieron los 21**: el contrato rige para los nuevos y para cualquiera que se toque por otro motivo.

### Lo que no se pudo medir

`auditoria_manuales.py` —la herramienta que contesta *"de N manuales, cuántos cumplen X"* contra una línea base— **no se pudo correr: esta máquina no tiene Python**. Las cifras de este paso (12 formas, 20 de 21, 4/2/2) salen de `grep` y lectura directa, y se declaran así en vez de presentarse como salida de la herramienta. Revisar N manuales sin rubro fijo son N impresiones; estas tres cifras son mediciones, pero con un instrumento más pobre.

---

## Entorno de Python — resuelto con `uv` · 2026-09-11

Decisión del PM: **`uv` es la vía declarada** para obtener el intérprete. Queda escrito en §2.3 de las reglas.

```
uv 0.11.9 · cpython 3.13.13 · ruta declarada con git config --local ingenieria.python
```

**Instalar Python no alcanzó, y esa es la parte que vale registrar.** Con `uv` instalado y 3.13.13 ejecutando correctamente, `command -v python3` **seguía encontrando el alias de la Microsoft Store** y `python3 -c ""` **seguía fallando**: los alias de `WindowsApps` están antes en el PATH y nada instalado después los desplaza. Por eso la ruta se **declara**, no se busca. La trampa del §11.2 de las reglas quedó ampliada con este dato, que es el que faltaba: *instalar la herramienta no arregla un PATH envenenado*.

### Lo que se destapó al haber Python

El `pre-commit` tiene dos motores y hasta hoy **sólo corría uno**. Al habilitar el segundo, se cayó:

```
ModuleNotFoundError: No module named 'comun'
```

**Y el hook interpretó la caída como "encontró un secreto".** El commit se frenó con el mensaje *"El revisor local encontro un secreto"*, que era falso: el revisor no encontró nada, se rompió antes de mirar.

**La causa fue un error propio del paso 2.** Copié `revisar_secretos.py` a `scripts/`, que es una de las rutas donde el hook lo busca — pero el script calcula `sys.path` como `parents[1]` de su propia ubicación y espera tener `comun/` de hermano. El diseño es `herramientas/seguridad/revisar_secretos.py` con `herramientas/comun/raiz.py` al lado. Corregido con `git mv`, preservando la historia, más `herramientas/comun/raiz.py`.

**Estuvo roto desde el paso 2 y nada lo avisó**, porque la ausencia de Python hacía que el motor se saltara entero con un aviso de "no corrió" que se leía como una limitación del entorno y no como un defecto.

### Verificación, ejecutando

| Qué | Antes | Ahora |
|---|---|---|
| `pre-push` → markdown | ok | ok |
| `pre-push` → agentes (sintaxis) | **NO SÉ** | **ok** — 25 de 25 archivos compilan |
| `pre-push` → web (build) | **NO SÉ** | **ok** |
| `pre-commit`, motores activos | gitleaks | **gitleaks + revisor-local** |
| Secreto inventado | frenado por 1 motor | **frenado por los 2** |

**Prueba de control de la comprobación de sintaxis**, porque un verde sin control no prueba nada: se metió a propósito un archivo con `def roto(:`. `compileall` devolvió **1**. Con todo sano devuelve **0**. No es un verde vacío.

Es la primera vez que algo verifica el Python de este repositorio.

### Candidato a subir al manual central (paso 9)

**Un escáner de seguridad que se cae no debería informar "encontró un secreto".** Frenar el commit está bien —fallar cerrado es lo correcto en un hook de seguridad—, pero el mensaje tiene que distinguir *"encontré esto"* de *"no pude mirar"*. El hook ya tiene ese vocabulario en el `pre-push`, donde un chequeo que no puede correr sale con `2 = NO SÉ`; el `pre-commit` no lo aplica a la caída de un motor. Un mensaje que atribuye un hallazgo inexistente manda a buscar un secreto que no existe.

---

## Secuencia de adopción

- [x] 0. Diagnóstico — 2026-09-11
- [x] 1. `/ingenieria:puntero` — 2026-09-11 · `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`)
- [x] 2. `/ingenieria:higiene` — 2026-09-11 · `.gitignore`, `.gitattributes`, `.githooks/`, `scripts/revisar_secretos.py`
- [x] 3. `/ingenieria:reglas` — 2026-09-11 · `docs/reglas/reglas_desarrollo.md`
- [x] 4. `/ingenieria:estructura` — 2026-09-11 · cero movimientos; `docs/roadmap.md` creada; carpetas ausentes declaradas
- [x] 5. `/ingenieria:readme-proyecto` — 2026-09-11 · 7 de 13 referencias al upstream corregidas; índice, estado, alcance y pruebas agregados
- [x] 6. `/ingenieria:manuales` — 2026-09-11 · 2 escritos, `SECURITY.md` partido, contrato de README de agente, 6 huecos declarados
- [ ] 7. `/ingenieria:auditoria`
- [ ] 8. `/ingenieria:seguridad`
- [ ] 9. `/ingenieria:cierre`
