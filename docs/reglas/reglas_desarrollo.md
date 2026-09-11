# 📐 Reglas de Desarrollo — `500-AI-Agents-Projects`

Este documento es la **fuente única de verdad** para el contexto del proyecto, su arquitectura, y los estándares de codificación, proceso y documentación.

Aplica por igual a personas y a cualquier LLM (Claude, Copilot, ChatGPT, Gemini…) que modifique este repositorio.

**Última revisión:** 2026-09-11 · **Audiencia:** quien contribuye código o documentación a este repositorio.

---

## 0. Jerarquía documental — qué manda sobre qué

Sin esto, dos documentos que se contradicen se resuelven por quien lo leyó último.

| Orden | Documento | Gobierna |
|---|---|---|
| 1 | El manual de ingeniería (repositorio central `etmunoz/ingenieria`) | **Cómo** se construye software. Doctrina general, independiente del dominio. |
| 2 | **Este documento** | Cómo se aplica el anterior a este repositorio. |
| 3 | [`docs/adopcion_ingenieria.md`](../adopcion_ingenieria.md) | Dónde estamos con la adopción. Documento **vivo**, no normativo. |

> **No hay fila de "fuente autoritativa del dominio".** Se borró a propósito: este repositorio no implementa una especificación, un contrato ni una norma externa. Lo que cada agente hace lo decide quien lo aporta, dentro de las reglas de acá.

**Resolución de conflictos:**

- Choque de **ingeniería** (estructura, proceso, documentación) → manda el manual central.
- Choque sobre **qué** hace un agente concreto → manda el `README.md` de ese agente, que es su contrato con quien lo ejecuta.
- Si el choque no se resuelve con esas dos reglas, **se detiene el trabajo y se consulta al PM.** No se elige en silencio.

---

## 1. Contexto del Proyecto

- **Nombre**: `500-AI-Agents-Projects`
- **Propósito**: un catálogo navegable de proyectos de agentes de IA (~118 entradas por framework y por industria) más 21 agentes ejecutables que sirven de ejemplo de referencia. Quien llega quiere una de dos cosas: encontrar un proyecto parecido al que tiene en mente, o clonar algo que corra hoy y modificarlo.
- **Operación**: local para los agentes (cada uno se ejecuta en la máquina de quien lo clona); GitHub Pages para el catálogo web. Sin servidor propio, sin usuarios, sin autenticación.
- **Idioma del código**: **inglés** para variables, comentarios, docstrings, nombres de carpeta y mensajes de commit. La documentación de proceso interno —este archivo, `docs/adopcion_ingenieria.md`, `AGENTS.md`— está en español. El catálogo y los README de agentes, en inglés: su audiencia es la comunidad.
- **Entorno**: Python ≥3.9, un entorno por agente con `pip` y `requirements.txt` — el intérprete se obtiene con **`uv`** (§2.3). Node ≥18 con `npm` para `web/`.
- **Interfaz**: CLI por agente (`uv run python agent.py`) + una SPA estática de catálogo.
- **Origen**: fork de `ashishpatel26/500-AI-Agents-Projects`. **Decisión del PM del 2026-09-11: este fork diverge.** No se agregan referencias nuevas al upstream; las **13 que quedan, repartidas en 6 archivos**, se reescriben en los pasos 5 y 8 de la adopción. Inventario línea por línea en [`docs/adopcion_ingenieria.md`](../adopcion_ingenieria.md).

### 1.1. Lo que este proyecto no es

- **No es un monorepo.** No hay `requirements.txt` en la raíz, ni entorno compartido, ni orquestador. Se decidió así para que cada agente se pueda copiar entero a otro lado y funcione. Ver §2.1.
- **No es una librería instalable.** Nada de `agents/` se publica en PyPI ni se importa desde afuera. Son ejemplos para leer, correr y modificar.
- **No es un producto con usuarios.** No hay cuentas, sesiones, ni datos persistentes de nadie. La SPA es estática y no tiene backend.
- **No hospeda modelos ni claves.** Cada quien trae las suyas. El repositorio nunca contiene una credencial funcionando.
- **El catálogo no pretende estar completo ni verificado entrada por entrada.** Es una lista curada de enlaces; que un proyecto figure no es un aval de que funcione.

> **Aplica: este repositorio es material didáctico y ejemplo de referencia.**
>
> Un proyecto que enseña tiene requisitos que uno normal no tiene, y **no son buenas prácticas opcionales: son el producto**.
>
> - **Cuando "más eficiente" choca con "más legible para quien nunca vio esto", gana la segunda**, y el motivo se escribe en el código. Un agente de 120 líneas que se entiende de una lectura vale más que uno de 60 que hay que descifrar.
> - **Nada es una caja negra.** Cada agente imprime qué recibió, qué decidió y qué devolvió. Un agente que funciona pero cuyo razonamiento no se puede exhibir **no cumple el requisito**, aunque el resultado sea correcto.
> - **Los errores son material.** Cuando falta una clave o el proveedor responde mal, el agente **muestra el fallo con su causa**, no lo esconde detrás de un "no se pudo procesar".
> - **Transportabilidad como requisito duro:** otra persona debe poder clonar, seguir el `README.md` del agente y tenerlo corriendo **sin acceso a esta máquina y sin preguntarle nada a nadie**. Es el criterio que decide si un aporte entra.

---

## 2. Stack Técnico

| Componente | Tecnología |
|---|---|
| Agentes | Python ≥3.9, un entorno y un `requirements.txt` por agente |
| Intérprete de Python | **`uv`** es la forma declarada de obtenerlo y de fijarlo. Ver §2.3 |
| Frameworks de agente | LangChain (12 agentes), CrewAI (4), LangGraph (3), LlamaIndex (1), sin framework (1) |
| Modelos | OpenAI `gpt-4o-mini` (14 agentes) y `gpt-4o` (6); un agente no usa modelo |
| Configuración | `python-dotenv` — los 21 agentes llaman a `load_dotenv()` |
| Catálogo web | React 18 + Vite 6, `lucide-react` para iconos |
| CI | GitHub Actions — 6 workflows |
| Linter de documentación | `markdownlint-cli2` con `.markdownlint-cli2.jsonc` |
| Hooks | `.githooks/` vía `core.hooksPath`; `gitleaks` en Docker + `herramientas/seguridad/revisar_secretos.py` |

### 2.1. Reglas de dependencias

- **Un manifiesto POR AGENTE, y ninguno en la raíz.** Esto **contradice a propósito** la regla de "un solo manifiesto" del manual central. El motivo: un agente tiene que poder copiarse entero fuera de este repositorio y seguir funcionando, y eso es lo que el proyecto vende. Un `requirements.txt` raíz lo rompería y además obligaría a resolver conflictos entre `crewai==0.80.0` y `langchain==0.3.0` que a nadie le importan, porque nunca conviven en el mismo entorno. Declarado en [`agents/README.md`](../../agents/README.md).
- **Versiones fijadas con `==` en los agentes.** Hoy 20 de 22 manifiestos lo hacen; los dos que usan `>=` son los del agente 21. Un ejemplo didáctico que deja de funcionar cuando el framework saca una versión mayor deja de ser un ejemplo.
- **No se agregan dependencias pesadas sin justificación.** Cada dependencia nueva es superficie de mantenimiento permanente. Se declara en el manifiesto del agente que la usa, nunca "por las dudas".
- **Nadie asume dónde está la raíz del proyecto.** Los agentes se ejecutan desde su propia carpeta (`cd agents/<x> && python agent.py`) y escriben ahí. Ninguna ruta absoluta en el código.

### 2.2. Verificación estática

| Herramienta | Comando | ¿Bloquea en CI? |
|---|---|---|
| `markdownlint-cli2` | `npx markdownlint-cli2` | **Sí** — `.github/workflows/markdown-lint.yml` |
| Verificador de enlaces | `lychee` sobre `README.md` | **Sí** — `.github/workflows/link-checker.yml`, pero **solo mira `README.md`**: los 22 README de `agents/` quedan fuera |
| DCO | sign-off en cada commit del PR | **Sí** — `.github/workflows/dco.yml` |
| Linter de Python | **no hay** | — |
| Verificador de tipos | **no hay** | — |
| Análisis de seguridad | **no hay** en CI; `gitleaks` corre en el `pre-commit` local | — |

**El estilo de Python se valida por revisión manual. Es un hueco declarado, no un olvido.** Ningún workflow ejecuta Python: el CI valida markdown, enlaces y sign-off, y nada más. Ver §6.

### 2.3. Python se maneja con `uv`, de punta a punta

Decisión del PM, 2026-09-11. `uv` es el gestor de entorno declarado del proyecto: obtiene el intérprete, crea el entorno virtual e instala las dependencias. **`requirements.txt` sigue siendo el manifiesto** (§2.1) — lo que cambia es quién lo lee.

**Nunca se instala con `pip` al Python del sistema.** Todo agente se instala dentro de su propio `.venv`, y esa es la regla que hace cierta la autocontención de §2.1: sin entorno por agente, `crewai==0.80.0` y `langchain==0.3.0` terminan en el mismo sitio.

```bash
# Una vez por máquina
uv python install
uv python list                                       # ver dónde quedó
git config --local ingenieria.python "<esa ruta>"    # declararlo, por clon

# Por agente
cd agents/<NN>-<nombre>
uv venv                                              # crea .venv/ acá
uv pip install -r requirements.txt
uv run python agent.py                               # usa .venv/ solo, sin activar
```

`uv run` resuelve el entorno local automáticamente: no hay paso de activación que olvidar, ni forma de instalar las dependencias de un agente en el entorno de otro.

**Y después hay que declararlo, una vez por clon**, o las herramientas del repositorio no lo encuentran:

```bash
git config --local ingenieria.python "<ruta que devolvió uv python list>"
```

Va en `--local` porque la ruta es de tu máquina: vive en `.git/config`, que no se versiona.

**Por qué hace falta declararlo y no alcanza con el PATH.** En Windows, `python` y `python3` están en el PATH como alias de la Microsoft Store que **fallan al ejecutarse**. Están antes que cualquier otra cosa, así que un intérprete instalado después no gana. Verificado el 2026-09-11 con uv ya instalado: `command -v python3` lo sigue encontrando y `python3 -c ""` sigue fallando. Ver §11.2.

**Esto rige también para la documentación pública.** Los 21 README de agente, el del curso y `CONTRIBUTION.md` documentan `uv venv` + `uv pip install` + `uv run python`, no `pip install`. Migrados el 2026-09-11.

**Por qué se documenta así y no con `pip` a secas:** los 21 README decían `pip install -r requirements.txt` **sin ningún paso de entorno virtual**. Al pie de la letra, eso instala 24 manifiestos con versiones fijadas y en conflicto —`crewai==0.80.0` junto a `langchain==0.3.0`— en el mismo Python del sistema. La autocontención que el proyecto promete existía en el árbol de archivos y no en las instrucciones.

**Verificación de versiones antes de fijar.** Toda versión nueva que entre a un `requirements.txt` tiene que existir en PyPI **y resolver junto con las demás del archivo**. No alcanza con que el paquete exista: ver §11.2, donde un manifiesto fijaba una versión que nunca se publicó.


---

## 3. Arquitectura de Módulos

Esta tabla se corrige en el mismo commit que crea o mueve un módulo.

| Carpeta | Función |
|---|---|
| `agents/` | Los 21 agentes ejecutables, uno por subcarpeta. Es donde está casi todo el código. |
| `agents/<NN>-<nombre>/` | Unidad autocontenida: `agent.py`, `metadata.yaml`, `requirements.txt`, `.env.example`, `README.md`. Los cinco archivos son obligatorios. |
| `crewai_mcp_course/` | Curso de 3 lecciones sobre CrewAI + MCP. Misma filosofía que un agente, sin `metadata.yaml`. |
| `web/` | SPA del catálogo (React + Vite). Se despliega sola a GitHub Pages en cada push a `main`. |
| `scripts/` | Utilidades con consumidor real en CI: `star-history.mjs` (lo llama `star-history.yml`) y `revisar_secretos.py` (lo llama el `pre-commit`). |
| `.githooks/` | `pre-commit` (secretos) y `pre-push` (comprobaciones), más `comprobaciones` con los comandos de este proyecto. |
| `images/` | Imágenes del README. `star-history.svg` lo **genera y commitea** el workflow, no se edita a mano. |
| `docs/` | Documentación de proceso interno: adopción, reglas. En español. |
| `.github/workflows/` | Los 6 workflows de CI. |
| ❌ `tests/` | **No existe.** No es una decisión: es el hallazgo 3 del diagnóstico. Ver §6. |
| ❌ `src/` o paquete raíz | **No existe a propósito.** Nada de este repositorio se importa desde afuera. Ver §1.1. |

**Dos reglas sobre esta tabla:**

- **Lo que se decidió NO construir se lista igual, con su motivo.** Una carpeta ausente sin explicación se interpreta como un olvido y alguien la crea.
- **Lo que todavía no existe se marca**, y la marca se quita **cuando el código existe y fue verificado** — no cuando se decidió que existiría.

### 3.1. Decisiones de arquitectura ya tomadas

| Fecha | Decisión | Motivo |
|---|---|---|
| heredada del upstream | Cada agente es autocontenido, sin monorepo | Se copia entero y funciona. Es lo que el repositorio vende. |
| heredada del upstream | `metadata.yaml` con 11 campos fijos (`title`, `description`, `author`, `language`, `framework`, `tags`, `industry`, `difficulty`, `llm`, `entrypoint`, `requirements`) | Alimenta el índice del catálogo. **Verificado: los 21 agentes usan exactamente los mismos 11 campos.** Agregar o quitar uno rompe el índice. |
| heredada del upstream | Numeración `NN-nombre-agent` con dos dígitos | Ordena la carpeta y da un identificador estable para enlazar. |
| 2026-09-11 | El fork **diverge** del upstream `ashishpatel26` | Decisión del PM. Ver §1. |
| 2026-09-11 | Los hooks viven en `.githooks/` versionado, no en `.git/hooks/` | Se revisan como código y no hay que re-copiarlos en cada clon. |
| 2026-09-11 | `.gitattributes` con `eol=lf` explícito en `.githooks/*` y `*.sh` | `core.autocrlf=true` a nivel sistema en Git para Windows. Un hook con CRLF falla en Linux y macOS y el repositorio queda sin protección **sin que nada lo avise**. Ver §11.2. |

---

## 4. Convenciones de Código

### 4.1. Encabezado de archivos

**Este proyecto NO usa el bloque de siete campos del manual central.** Cada `agent.py` abre con un docstring de módulo que dice qué hace el agente y con qué framework. Los 21 lo hacen; ninguno tiene el bloque de siete campos.

**Se conserva la convención del proyecto, y el motivo es el propósito del repositorio:** cada `agent.py` está escrito para leerse de corrido como ejemplo, y siete líneas de metadatos de proceso antes de la primera línea de enseñanza le restan exactamente a lo que el archivo existe para hacer. La trazabilidad que el bloque aporta ya está en `metadata.yaml` (autor, entrypoint) y en el historial de git (fechas).

Lo que sí es obligatorio en el docstring de módulo:

```python
"""
<Nombre del agente> using <framework> + <servicios externos>.

<Dos o tres líneas de qué hace y en qué orden.>

Run:
    pip install -r requirements.txt
    cp .env.example .env
    python agent.py
"""
```

### 4.2. Documentación en el código

- Toda función no trivial lleva docstring con **Objetivo / Entrada / Salida**, y qué errores lanza.
- No se eliminan docstrings existentes salvo que su contenido sea incorrecto.
- **Se explica lo no obvio, no lo evidente.** En este repositorio hay una excepción deliberada: cuando un comentario explica un concepto del framework que quien lee puede no conocer, **se queda aunque parezca obvio para quien ya sabe**. Es material didáctico (§1.1).

### 4.3. Naming

Prioridad explícita, en este orden: (1) nombre dado por quien pide el trabajo — siempre gana; (2) entidad principal del requerimiento; (3) patrón estructural; (4) operación principal, como último recurso.

Para carpetas de agente: `NN-<qué-hace>-agent`, dos dígitos, minúsculas, guiones. El sufijo `-agent` se omite cuando el nombre ya lo implica (`15-unit-test-generator`, `20-multi-agent-debate`).

### 4.4. Tamaño de archivo

Un archivo, una responsabilidad. Evaluar partición cerca de las **500 líneas**; tratarlo como deuda técnica activa por encima de las **1.000**.

**Medición al 2026-09-11** (`wc -l`):

- Los 21 `agent.py` están holgadamente por debajo: el mayor es `agents/16-documentation-writer/agent.py` con **202** líneas. Total 2.622 (medido 2026-09-11, después de agregar las guardas de codificación).
- `web/src/App.jsx` tiene **1.057 líneas** — **por encima del umbral de deuda técnica activa.** Queda declarado acá; partirlo no es trabajo de la adopción.
- `web/src/content.js` tiene **512** líneas: en la zona de "evaluar partición". Es una tabla de datos, así que crecer es su naturaleza.

---

## 5. Configuración, Datos y Secretos

- **Los secretos van en variables de entorno**, nunca en el código ni en el historial. Los 21 agentes usan `load_dotenv()` y leen con `os.getenv()`.
- **`.env` está en `.gitignore` y nunca se commitea con valores reales.** `.env.example` sí se versiona: hay 24 y son el contrato de configuración.
- **`.env.example` es obligatorio y se mantiene al día.** Toda variable nueva se agrega ahí **en el mismo commit** que la introduce, con un comentario de qué es y de dónde se saca.
- **Ninguna clave se imprime.** Verificado al 2026-09-11: ningún `agent.py` imprime una credencial.
- **Los patrones de exclusión se anclan a la ruta exacta.** Ver los comentarios del [`.gitignore`](../../.gitignore): `/web/node_modules/` y no `node_modules/`; las salidas de agentes por ruta completa y no `*.csv`. Un patrón suelto esconde código real, y excluir de más se ve idéntico a estar bien configurado.
- **`test_*.py` NO se ignora**, aunque el agente 15 lo genere. El patrón escondería las pruebas reales el día que existan.
- **Cada clon nuevo tiene que activar los hooks a mano**: `core.hooksPath` vive en `.git/config`, que no se versiona.

```bash
git config core.hooksPath .githooks
```

---

## 6. Pruebas y Calidad

> [!WARNING]
> **Este repositorio no tiene ni una sola prueba.** Medición al 2026-09-11: **0 archivos de test entre 170 versionados**, y ningún workflow de CI ejecuta Python. Son 2.622 líneas de agentes que no verifica nada. Lo que sigue es la regla que rige **desde ahora**, no una descripción del estado actual.

- **Framework y comando cuando existan**: `pytest`, ejecutado desde la carpeta del agente (`python -m pytest -q`). `pytest==8.3.0` ya figura en el manifiesto del agente 15.
- **Ubicación**: el test de un agente vive junto a su `agent.py`, nombrado `test_<algo>.py`. No hay `tests/` centralizado: rompería la autocontención (§2.1).
- **La suite corre completamente offline.** Ningún test llama a OpenAI, Tavily, NewsAPI, GitHub ni TrustBoost. Un test que depende de un proveedor externo falla de forma intermitente y entrena a todos a ignorar los fallos.
- **Definición de terminado para cobertura:**
  - Cada bug corregido deja un **test de regresión que falla con el código anterior y pasa con el corregido**.
  - Cada agente nuevo lleva al menos un test que verifique que arranca y falla con mensaje claro **cuando la clave no está**. Es el fallo más frecuente de quien clona.
- **Un refactor "sin cambio de comportamiento" sólo se confirma corriendo la suite completa antes y después.**
- **Clasificar el fallo antes de declarar una regresión**: ¿es código, entorno, versión del runtime, o el `venv` equivocado? En este repositorio el sospechoso número uno es el entorno: cada agente tiene el suyo.
- **Verde es una afirmación sobre lo que el chequeo mira, nunca sobre el sistema.** El `pre-push` de este repositorio lo aplica al pie de la letra: una comprobación que no puede correr sale con código **2 = NO SÉ**, nunca con 0. Hoy dos de las tres están en ese estado.

---

## 7. Reporte de Estado

El error caro no es equivocarse: es **afirmar más de lo que se midió**.

- **Ninguna afirmación desnuda.** Todo estado se reporta con la cifra medida y el comando que la produjo:

  ```
  markdown: 26 archivos / 0 hallazgos   (npx markdownlint-cli2, 2026-09-11 10:14)
  ```

  Nunca "eso ya funciona bien".

- **El comando tiene que ser el de la herramienta que decide**, no uno auxiliar que la aproxima. En este repositorio la trampa concreta: `command -v python` **encuentra** el alias de la Microsoft Store, que falla al ejecutarse. Se prueba con `python -c ""`, no se pregunta si está. Ver §11.2.

- **Los tres estados, nunca dos:**

  | Estado | Qué prueba | Qué NO prueba |
  |---|---|---|
  | **Compila / valida** | La sintaxis y los tipos son válidos | Nada sobre el comportamiento |
  | **Integra / enlaza** | Las piezas encajan y todo resuelve | Que resuelvan a lo correcto |
  | **Funciona** | Se observó el comportamiento esperado corriendo | — |

  Un agente "escrito y que importa limpio" está en el estado 1 de 3. **Un agente no se declara funcionando hasta que alguien lo corrió con una clave real y vio la salida.**

- **Informar qué se probó y qué no**, con cifras reales y riesgos pendientes.

### 7.1. Reproducibilidad

- **Criterio de aceptación del catálogo web:**

  ```bash
  rm -rf web/node_modules web/dist && npm --prefix web ci && npm --prefix web run build
  ```

- **Criterio de aceptación de un agente:** en la carpeta del agente, sin `.venv` previo,

  ```bash
  uv venv --clear && uv pip install -r requirements.txt && cp .env.example .env && uv run python agent.py
  ```

  tiene que llegar hasta el mensaje de "falta la clave" sin ningún otro error. **El paso de instalación es parte del criterio, no un preámbulo**: es exactamente el que estuvo fallando sin que nadie lo notara en el agente 01 (§11.2).
- Todo artefacto derivado es **regenerable desde su fuente**, no se corrige a mano. `images/star-history.svg` lo produce `scripts/star-history.mjs`: editarlo a mano lo pisa el workflow en el próximo lunes.

---

## 8. Control de Versiones y Commits

- **Flujo**: trunk-based sobre `main`. Rama corta por tarea, PR, merge. Una rama abierta durante semanas diverge cada vez más.
- **Mensajes**: Conventional Commits **en inglés**, minúsculas, sin punto final: `tipo(alcance): descripción`. En inglés porque el historial es público y la audiencia del repositorio es internacional — a diferencia de `docs/`, que va en español (§1).
- **Todo commit lleva `Signed-off-by` que coincida con su autor.** Lo exige `.github/workflows/dco.yml` en cada PR. `git commit -s` lo agrega solo.
- **Un commit, un propósito.** No se mezclan limpieza del repositorio, cambio funcional y evidencia operativa.
- **Staging explícito, nunca `git add .`** Los archivos se agregan por su ruta. Evita colar una credencial o un artefacto generado, y obliga a revisar conscientemente qué entra.
- **Preservar la historia al mover o renombrar**: `git mv`, no borrar y recrear.
- **Operaciones destructivas, con confirmación explícita de una persona.** Incluye **no saltarse los hooks**: si el `pre-commit` bloquea, se investiga la causa, no se usa `--no-verify`.
- **Ningún commit ni push por iniciativa propia de un agente.** Cada operación que publique o fije un estado requiere instrucción explícita del PM **en ese momento**, aunque ya lo haya pedido antes en la sesión.

  > **Excepción vigente, acotada:** el 2026-09-11 el PM autorizó de forma permanente documentar, commitear y pushear **cada paso de la secuencia de adopción del manual de ingeniería**, sin volver a preguntar entre paso y paso. La excepción **se agota al cerrar el paso 9** y no se extiende a ningún otro trabajo. Una autorización permanente que nadie escribió es indistinguible de una que nadie dio.

---

## 9. Seguridad

Las prácticas generales están en el manual central. Acá van las **decisiones de este proyecto**:

- **Modelo de amenaza en una línea:** se protege la **clave de API de quien clona** —de que entre al historial por accidente— y la **integridad del código que se publica**, de que alguien inserte algo dañino en un ejemplo que otros van a ejecutar en su máquina. Se asume confiable: GitHub Actions, los registros de paquetes (PyPI, npm) y los proveedores de modelos.
- **Ningún dato sensible en logs**: tokens, contraseñas, credenciales, ni cuerpos completos de petición o respuesta con datos adentro.
- **Todo hallazgo de seguridad se corrige vía un plan, nunca ad-hoc.**
- **El modelo de amenaza** está en [`docs/manuales/manual_seguridad.md`](../manuales/manual_seguridad.md) y el **registro de riesgos** en [`docs/manuales/manual_riesgos.md`](../manuales/manual_riesgos.md).

> **Aplica: este proyecto NO tiene usuarios ni autenticación.**
>
> Declarado el 2026-09-11. Motivo: los agentes son herramientas de una sola persona que corren en su propia máquina, y el catálogo web es estático y sin backend. No hay cuentas, sesiones ni datos de nadie.
>
> **Que no haya autenticación no elimina los controles que siguen vigentes**, y son tres:
>
> 1. **El código que publicamos se ejecuta en la máquina de otra gente.** Es la superficie real de este repositorio. Un `agent.py` aportado por un tercero puede hacer cualquier cosa en la máquina de quien lo corra: se revisa línea por línea antes de aceptarlo.
> 2. **El presupuesto de quien clona.** Un agente con un bucle sin corte quema el crédito de OpenAI de otra persona. Todo bucle de agente declara su tope de iteraciones.
> 3. **La clave de quien clona.** Es lo que protege el `pre-commit` y el `.gitignore`.

> **Aplica: este proyecto trata datos personales.**
>
> Dos agentes los tocan por diseño, y hay que decirlo:
>
> - **`09-resume-parser-agent`** recibe currículums —nombre, contacto, historia laboral— y los manda a OpenAI.
> - **`21-pii-sanitization-agent`** recibe texto con PII y lo manda a `https://api.trustboost.dev`, un tercero.
>
> Reglas que salen de eso:
>
> - **Ningún dato personal real entra al repositorio.** Los ejemplos, fixtures y capturas usan datos inventados. Un CV de verdad en un archivo de ejemplo es una filtración, aunque sea el propio.
> - **El README de un agente que manda datos a un tercero lo dice en su primera pantalla**, con el destino nombrado. Quien lo ejecuta tiene que poder decidir antes, no descubrirlo leyendo el código.
> - **Procedencia y destino viajan con el dato**: qué se manda, a quién, y qué se asume que hace con eso.

---

## 10. Planes, Revisiones y Documentación

### 10.1. Planes de trabajo

- **Ubicación y nombre**: `docs/planes/plan_<conceptos>_<AAAAMMDD>_<HHMM>.md`. 🚧 La carpeta todavía no existe. El paso 4 la declaró como "no se usa todavía", con su costo escrito: el trabajo de una sesión sobrevive en el mensaje de commit, el que abarque varias se pierde. Se crea con el primer trabajo que no entre en una sesión.
- **Estructura**: indicación inicial de leer este documento; título; metadatos (fecha y hora de creación y de última actualización, autor, objetivo, impactos); desarrollo con detalle técnico real; checklist de tareas incluyendo pruebas; y qué documentos hay que actualizar al terminar.
- **Rigor proporcional al riesgo.** Agregar un agente nuevo admite un plan liviano: alcance en una línea, los cinco archivos obligatorios, cómo se valida. Cambiar el esquema de `metadata.yaml` —que alimenta el índice del catálogo— exige plan completo, porque toca los 21. Lo que se reduce es el formalismo, **nunca la trazabilidad**.
- **Marcado del avance (obligatorio).** Cada casilla se marca **en el mismo commit que completa esa tarea**. Un plan no se cierra ni se archiva con una casilla sin marcar. Si una tarea se difiere, **no se marca**: queda sin marcar con una anotación del motivo.

### 10.2. Revisiones (walkthroughs)

- **Ubicación y nombre**: `docs/revisiones/walkthrough_<conceptos>_<AAAAMMDD>_<HHMM>.md`. La carpeta **existe** desde el paso 7, que dejó ahí la auditoría de código. Todavía no hay ningún walkthrough: el primero llega con el primer plan.
- **Contenido**: qué se hizo (archivos creados/modificados), qué se probó, y el resultado real de la validación.

### 10.3. Archivado, con auditoría previa

- **Antes de archivar un plan y su walkthrough, releer el walkthrough completo** buscando hallazgos, decisiones diferidas o cabos sueltos que hayan surgido durante la ejecución.
- **Si aparece uno, no se archiva en silencio**: se redacta un plan nuevo. *Un hallazgo anotado no es un pendiente gestionado.*
- Recién después se archiva con `git mv`, corrigiendo las referencias que queden apuntando a la ruta anterior.

### 10.4. Requerimientos

**No hay registro único de requerimientos, y por ahora no hace falta.** Lo que este repositorio recibe son aportes de agentes, no requerimientos: el contrato de cada aporte es el `README.md` del agente y los cinco archivos obligatorios de §3. Si algún día hay trabajo que no sea "agregar o arreglar un agente", se crea el registro y se escribe acá.

### 10.5. La documentación es parte del cambio

Un cambio no está terminado si la documentación que afecta sigue describiendo el estado anterior. Como mínimo: [`AGENTS.md`](../../AGENTS.md), [`README.md`](../../README.md), [`agents/README.md`](../../agents/README.md) —que trae el índice de los 21—, **este propio documento si el cambio introdujo una convención nueva**, y el `README.md` del agente tocado.

**Un agente nuevo toca tres documentos, no uno:** su propio README, el índice de `agents/README.md`, y la tabla del catálogo en `README.md`.

> **Aplica: en este repositorio los documentos SON el producto.**
>
> El catálogo y los README de agentes no son documentación de apoyo: son **la superficie del sistema**. Estar desactualizado deja de ser "un documento viejo" y pasa a ser **una respuesta equivocada** para alguien que no nos puede preguntar.
>
> - **El README de un agente es el manual de usuario de este proyecto.** No hay otro. Por eso sus secciones son un contrato con nombres exactos —`Setup`, `Run`, `Output`, `Cost`, `Limits`—, declarado en [`CONTRIBUTION.md`](../../CONTRIBUTION.md). Medición al 2026-09-11: los 21 existentes usan **12 formas distintas**; el contrato rige para los nuevos y para cualquiera que se toque por otro motivo.
> - Todo documento lleva **encabezado con audiencia y fecha de última revisión**. 🚧 Al 2026-09-11 lo tienen los de `docs/`; **ninguno de los 26 `.md` de la raíz y de `agents/`**. Deuda declarada del diagnóstico, no una regla ya cumplida.
> - Todo enlace tiene que resolver. El verificador de enlaces de CI **sólo mira `README.md`**: los 22 README de `agents/` se revisan a mano hasta que eso cambie.

---

## 11. Capitalizar el Error que Cuesta Tiempo (obligatorio)

**Un error que se repite deja de ser un error: es una superficie sin defensa.**

Cuando algo hace perder tiempo, **no basta con arreglarlo**. Antes de cerrar el tema, tres preguntas en este orden:

1. **¿Qué se perdió?** No el error: **el tiempo**.
2. **¿Por qué el sistema lo permitió?** La causa inmediata casi nunca es la interesante. Se arregla la estructural.
3. **¿Qué impide que vuelva a pasar sin depender de que alguien se acuerde?** Un test, un detector, una tolerancia en el código. **Una nota que dice "tener cuidado con X" no cumple esta regla: la disciplina no es un mecanismo.**

**Cuándo aplica:** a partir de la **segunda vez**.

**Dónde se escribe cada parte:** la lección genérica → al manual central; el detalle operativo → acá abajo; **el mecanismo → al código**, que es la única de las tres que actúa sola.

### 11.1. La ocurrencia y la forma

**El arreglo es mínimo; el barrido es completo.** Antes de dar por cerrado un arreglo, preguntar: *¿qué otra cosa comparte esta propiedad?* La respuesta se busca con una **enumeración mecánica** sobre todo el proyecto, no repasando de memoria. Acá eso casi siempre significa: *si le pasa a un agente, ¿les pasa a los 21?* **El resultado se escribe aunque dé cero.**

### 11.2. Trampas que ya costaron tiempo

| Trampa | Síntoma | Causa real | Mecanismo que la detecta hoy |
|---|---|---|---|
| **`.gitignore` inexistente, y `SECURITY.md` afirmando lo contrario** | Ninguno: todo se ve bien hasta que una clave está en el historial | `SECURITY.md:36` decía que los `.env` estaban ignorados "by default". No había `.gitignore` en ningún nivel. La documentación no omitía la protección: **aseguraba que existía**, así que nadie la revisaba | [`.gitignore`](../../.gitignore) + hook `pre-commit` con `gitleaks`. Probado intentando commitear una clave inventada: frenó con `leaks found: 2` |
| **Hooks sin bit de ejecución** | En Windows funciona perfecto. En Linux y macOS git **omite el hook en silencio** y el repositorio queda sin protección de secretos | `core.filemode=false` en Git para Windows: el `chmod +x` no se registra en el índice. Se commiteó `100644` | Los modos se fijaron a `100755` con `git update-index --chmod=+x` y se verificaron **en un clon limpio**, no leyendo el índice local |
| **CRLF en scripts POSIX** | `bad interpreter` en Linux y macOS; en Windows no pasa nada | `core.autocrlf=true` a nivel **sistema** en Git para Windows. Sin `.gitattributes`, cada clon decide solo. MSYS tolera el `\r`, que es peor: en Windows parece que funciona | [`.gitattributes`](../../.gitattributes) con `eol=lf` explícito en `.githooks/*` y `*.sh` |
| **`command -v python` encuentra un Python que no existe** | La comprobación de secretos informaba "no corrió" en vez de fallar, o peor, un chequeo salía verde sin haber corrido | En Windows, `python` y `python3` están en el PATH como **alias de la Microsoft Store** que fallan al ejecutarse. `command -v` los encuentra y los da por buenos. **Instalar Python no lo arregla:** los alias siguen antes en el PATH. Verificado el 2026-09-11 con `uv` ya instalado y 3.13.13 funcionando — `command -v python3` seguía encontrando el alias y `python3 -c ""` seguía fallando | El intérprete se **prueba** con `-c ""`, no se pregunta si está; y se **declara por ruta** con `git config --local ingenieria.python` en vez de confiar en el PATH (§2.3). Toda comprobación que no puede correr sale con **2 = NO SÉ**, nunca con 0 |
| **El README manda a clonar otro repositorio** | Quien sigue el Quick Start al pie de la letra termina en el fork de otra persona; quien reporta una vulnerabilidad —o una conducta— la manda al correo de otra persona | Fork de `ashishpatel26` con **13 referencias al original intactas en 6 archivos** | **Resuelto el 2026-09-11**: las 13 reescritas o retiradas en los pasos 5 y 8. Los reportes de seguridad van al advisory privado de este repositorio. El mecanismo que queda es la regla de §1 — no agregar referencias nuevas al upstream |
| **El agente de referencia no se podía instalar, y nadie lo sabía** | `agents/01-web-research-agent` —el primero que el README manda a correr y el que `CONTRIBUTION.md` llama "la referencia"— fallaba al instalar con un error de resolución, con `pip` y con `uv` por igual | `requirements.txt` fijaba `langchain-tavily==0.1.0`, **una versión que nunca se publicó**: la más antigua en PyPI es la 0.1.5. Y `langchain-core==0.3.0` era a su vez demasiado viejo para cualquier `langchain-tavily` existente, así que el manifiesto era **internamente insatisfacible**. Sobrevivió porque **nada instala nada**: el CI no ejecuta Python y no hay pruebas | Barrido de los 104 pines de los 24 manifiestos contra la API de PyPI, 2026-09-11 — este era el único. Regla nueva en §2.3: una versión no se fija sin comprobar que existe **y que resuelve con las demás del archivo**. El mecanismo que falta es un chequeo de instalación en CI, y está declarado como deuda en §6 |
| **Contar con un `grep` demasiado estrecho** | El informe del paso 0 afirmó "nueve referencias al upstream en cuatro archivos". El número real es **13 en 6** | El `grep` sólo miraba `*.md` y sólo el patrón `ashishpatel26`. Se le escaparon el correo del mantenedor original (`ashishpatel.ce.2011@`) en dos archivos, y una regla en un `.yml`. **Una cifra medida con el filtro equivocado se ve exactamente igual que una bien medida** | Todo inventario que vaya a un documento se escribe con el comando que lo produjo al lado, y el comando cubre **todas** las extensiones y **todos** los patrones del concepto, no el más obvio. Ver §7 |

---

## 12. Comandos Frecuentes

**Shell de referencia: `bash`** (Git Bash en Windows). Es lo que usan el `README.md`, los hooks —que son POSIX `sh`— y los runners de CI, que corren en `ubuntu-latest`. No se mantienen equivalencias en PowerShell: un comando que sólo funciona en el shell de quien lo escribió es una trampa para el siguiente.

```bash
# ── Preparar el clon: DOS cosas, ninguna se versiona ──────────────────
git config core.hooksPath .githooks                  # 1. activar los hooks
uv python install                                    # 2. obtener el intérprete
uv python list                                       #    ver dónde quedó
git config --local ingenieria.python "<esa ruta>"    #    y declararlo

# Comprobar que el intérprete declarado REALMENTE ejecuta
"$(git config --get ingenieria.python)" -c "" && echo ok

# Correr un agente — nunca se instala al Python del sistema
cd agents/01-web-research-agent
uv venv                          # crea .venv/ acá, sólo para este agente
uv pip install -r requirements.txt
cp .env.example .env             # y poner la clave
uv run python agent.py           # usa .venv/ sin activarlo

# Rehacer el entorno de un agente desde cero
uv venv --clear && uv pip install -r requirements.txt

# Sintaxis de los 25 archivos Python, sin instalar dependencias
"$(git config --get ingenieria.python)" -m compileall -q agents crewai_mcp_course

# Catálogo web en desarrollo
npm --prefix web ci
npm --prefix web run dev

# Construir el catálogo para producción
npm --prefix web run build

# Linter de documentación — lo mismo que corre el CI
npx markdownlint-cli2

# Las comprobaciones del pre-push, sin publicar
sh .githooks/pre-push

# Declarar dónde está Python si no quedó en el PATH (por clon)
git config --local ingenieria.python /ruta/al/python
```

---

## 13. Checklist de Contribución (Definition of Done)

- [ ] Docstring de módulo con nombre, framework y bloque `Run:` (§4.1)
- [ ] Docstrings Objetivo/Entrada/Salida en toda función no trivial (§4.2)
- [ ] Variables de entorno nuevas agregadas al `.env.example` **en el mismo commit** (§5)
- [ ] Sin credenciales ni datos personales reales en el repositorio (§5, §9)
- [ ] Sin datos sensibles en logs (§9)
- [ ] Tests agregados o actualizados, y la suite en verde (§6)
- [ ] La suite sigue corriendo **sin red y sin servicios externos** (§6)
- [ ] Sin dependencias nuevas sin justificación, con versión fijada con `==` (§2.1)
- [ ] Commit con propósito único, mensaje en inglés según la convención, y `Signed-off-by` (§8)
- [ ] Staging explícito por ruta, nunca `git add .` (§8)
- [ ] Documentación afectada actualizada, incluido este documento si cambió una regla (§10.5)
- [ ] Un agente nuevo actualizó **los tres** documentos: su README, el índice de `agents/README.md` y la tabla de `README.md` (§10.5)
- [ ] Si una sección marcada 🚧 dejó de serlo porque el código existe **y se verificó**, se le quitó la marca (§3)
- [ ] Si el trabajo nació de un error que costó tiempo: **mecanismo** que lo detecta, no sólo el arreglo del síntoma (§11)
- [ ] `npx markdownlint-cli2` en verde (§2.2)
- [ ] Verificación cruzada final contra lo que se pidió originalmente

**Ítems adicionales para un agente nuevo** (§1.1, §3):

- [ ] Los cinco archivos obligatorios: `agent.py`, `metadata.yaml`, `requirements.txt`, `.env.example`, `README.md`
- [ ] `metadata.yaml` con los **once** campos, ninguno de más ni de menos
- [ ] Se clonó en una carpeta limpia y se corrió siguiendo sólo el README, sin preguntarle nada a nadie (§1.1)
- [ ] Todo bucle de agente declara su tope de iteraciones (§9)
- [ ] Si manda datos a un tercero, el README lo dice **en su primera pantalla**, con el destino nombrado (§9)

---

# Anexo — Bloques condicionales por rasgo del proyecto

## A. Interfaz web — `web/`

**El estándar visual es normativo desde el primer componente**, no un ajuste posterior.

- **Los botones se categorizan por su efecto**, no por su lugar en la pantalla: los que **ejecutan o cambian algo** se ven de una manera, los que **sólo leen o exportan** de otra. En esta SPA casi todo es lectura y navegación: cualquier control que en el futuro dispare algo tiene que distinguirse de los actuales.
- **Un mismo tipo de botón se ve igual en *todos* sus usos.** Antes de copiar el estilo de un botón existente, comparar contra **todos** los de esa categoría, no sólo contra el más cercano.
- **Un patrón visual que se repite se extrae a un componente compartido apenas se detecta la segunda repetición.** Acá tiene nombre y medida: `web/src/App.jsx` son **1.057 líneas en un solo archivo** (§4.4). Es exactamente la forma en que una interfaz acumula copias divergentes sin que nadie lo decida.
- **Los errores se muestran donde ocurrieron**, con un componente común.
- **La interfaz no crece más rápido que el motor.** Antes de mejoras visuales se privilegia, en este orden: robustez del núcleo, consistencia semántica, calidad del diseño, trazabilidad, testabilidad.
- **Variables build-time vs. runtime:** Vite **hornea** las variables `VITE_*` dentro del bundle durante `npm run build`. Cambiarlas después no tiene ningún efecto. Este sitio se despliega a GitHub Pages desde `jekyll-gh-pages.yml`: toda variable nueva tiene que estar disponible **en el momento del build del workflow**, no en el entorno de Pages.

## E. Componentes con LLM o modelos

Es el rasgo central de este repositorio: 20 de los 21 agentes llaman a un modelo.

- **Nunca confiar en que el modelo respetó el formato pedido.** Normalizar y validar la salida contra el conjunto de valores conocido **inmediatamente al recibirla**. Si no coincide con ninguno, asignar un valor "desconocido" **distinguible** — nunca dejar que caiga en el mismo camino que un valor conocido y seguro.

  > **Medición al 2026-09-11: sólo 4 de los 21 agentes validan la salida del modelo** (Pydantic, `with_structured_output` o `json.loads` con manejo de error). Los otros 17 la consumen tal cual. Es deuda declarada, y el criterio para lo que entre de ahora en adelante.

- **Los componentes con modelo se testean por contrato, no por contenido.** Se verifica que la salida cumpla el esquema, que una respuesta basura se maneje sin romper el flujo, y que el fallo quede registrado. **No se afirma que el modelo dé una respuesta concreta**: eso falla de forma intermitente, que es peor que no existir.
- **Que el proveedor esté caído es un caso de prueba, no un imprevisto.** Y en un repositorio didáctico tiene una consecuencia extra: el mensaje de error es lo primero que ve quien clona sin clave. Tiene que decir qué falta y dónde ponerlo.
- **El prompt de sistema se asume descubrible**: no lleva secretos, credenciales ni nombres sensibles.
- **La agencia se verifica, no se supone**: lo que el modelo puede efectivamente disparar se enumera y se prueba, no se deduce de cómo está escrito el prompt.
- **Nada generado por un modelo se ejecuta sin validación determinista previa.** La validación es **código**, no una instrucción en el prompt.

  > Al 2026-09-11 ningún `agent.py` usa `exec`, `eval`, `subprocess`, `os.system`, `PythonREPL` ni `shell=True` — verificado con `grep` sobre los 25 archivos. **Esa propiedad se mantiene.** Un agente que quiera ejecutar código generado necesita aprobación explícita del PM y una capa de validación escrita en Python.

- **Todo bucle de agente declara su tope de iteraciones.** Quien clona paga los tokens (§9).
- **El costo se registra**: al menos qué modelo usa y cuántas llamadas hace por ejecución, en el README del agente.

## F. Fuentes de datos externas o de terceros

Los agentes hablan con OpenAI, Tavily, NewsAPI, la API de GitHub, yfinance y TrustBoost.

- Los componentes que hablan con el exterior viven **aislados**, para que su inestabilidad inherente no contamine el resto del agente.
- **Cada unidad captura sus propias excepciones**: un fallo procesando un elemento no puede tumbar el lote.
- **La cobertura se cuenta y se reporta**: cuántos se procesaron, cuántos fallaron y cuáles. Un lote que informa sólo "terminado" oculta justo lo que hay que ver.
- **El límite de paralelismo lo pone el tercero, y su señal es su error, no tu reloj.**
- **Procedencia y edad del dato** viajan con el dato. Importa especialmente en `11-stock-research-agent` y `06-news-summarizer-agent`, donde un dato viejo presentado como actual es una respuesta equivocada, no un dato viejo.

## I. Librería, CLI o lenguaje/DSL

Cada agente es una CLI. Aunque no se instale como paquete, el contrato de línea de comandos es lo que usa quien lo clona.

- **La ayuda del comando es documentación de primera clase**, no un texto residual. Todo `add_argument` lleva `help=`.
- **Los códigos de salida son parte del contrato**: distinguir "falló" de "no encontró" de "no pude ejecutar". El caso concreto y más frecuente: **falta la clave de API** tiene que ser distinguible de **el modelo devolvió algo inservible**.
- **Los valores por defecto se documentan en el README**, porque son lo que corre cuando alguien ejecuta `python agent.py` sin argumentos — que es lo que hace todo el mundo la primera vez.
