# AGENTS.md — Punto de entrada de `500-AI-Agents-Projects`

> [!IMPORTANT]
> Si acabás de llegar a este repositorio —persona o LLM—, **detené cualquier generación de código**.
> Leé primero, en este orden:
>
> 1. **[`docs/reglas/reglas_desarrollo.md`](docs/reglas/reglas_desarrollo.md)** — cómo se trabaja **en este repositorio**. Lectura obligatoria; prevalece sobre cualquier costumbre general. Las cinco reglas duras de más abajo son su resumen, no un sustituto.
> 2. **[`README.md`](README.md)** — qué es esto: un catálogo de agentes de IA más 21 implementaciones ejecutables.
> 3. **[`agents/README.md`](agents/README.md)** — la convención de los agentes, que es donde está casi todo el código.
> 4. **[`docs/adopcion_ingenieria.md`](docs/adopcion_ingenieria.md)** — en qué estado está la adopción del manual de ingeniería, qué se midió y qué queda abierto.
> 5. **El manual de ingeniería** — central, no vive acá. Ver la última sección.

Este archivo existe porque **las reglas que nadie encuentra no se cumplen**. Antes de él, quien entraba por la raíz no tenía ningún puntero hacia las reglas del proyecto ni hacia el manual.

---

## Lo mínimo que hay que respetar

**1. No commitees un `.env`. Y no confíes en que algo te va a frenar.**

Hoy **no existe ningún `.gitignore` en este repositorio**, en ningún nivel, y no hay hooks instalados. Al mismo tiempo hay 24 carpetas con `.env.example` y la documentación te dice `cp .env.example .env` como paso de arranque. Un `git add .` sube tu clave de OpenAI y nada lo intercepta.

Peor: [`SECURITY.md`](SECURITY.md) afirma que los `.env` "are gitignored by default". **Es falso.** Está anotado como hallazgo 1 del diagnóstico y lo repara el paso 2 (`/ingenieria:higiene`). Hasta entonces, agregá archivos por nombre —`git add ruta/al/archivo`— nunca en lote.

**2. Este fork diverge del upstream.** Decisión del PM del 2026-09-11. El repositorio nació como fork de `ashishpatel26/500-AI-Agents-Projects` y quedan **13 referencias al original, repartidas en 6 archivos**: `README.md` (4 badges, el `git clone` del Quick Start, el gráfico de estrellas, el pie con "Report Issue"), `SECURITY.md` (correo y advisory), `CODE_OF_CONDUCT.md` (correo de denuncias), las dos plantillas de issue (`assignees`) y `link-checker.yml` (una regla que excluye la URL del upstream). El inventario línea por línea está en [`docs/adopcion_ingenieria.md`](docs/adopcion_ingenieria.md). Se reescriben a `etmunoz/` en los pasos 5 y 8. **No agregues referencias nuevas al upstream**, y si tocás alguna de las que quedan, corregila de paso.

**3. Cada agente es autocontenido, y así se queda.** Su propio `requirements.txt`, su propio `.env.example`, su propio `README.md`, ejecutable con `python agent.py` sin preparar nada más. No hay `requirements.txt` en la raíz y no debe haberlo: es una decisión explícita de [`agents/README.md`](agents/README.md) y es lo que hace que el repositorio sirva para lo que sirve.

**4. Lo que afirmes de un agente, verificalo ejecutándolo.** Este repositorio **no tiene ni una sola prueba** —0 archivos de test entre 145 versionados— y el CI nunca ejecuta Python: valida markdown, enlaces del README y el sign-off de los PR, nada más. Son 2.482 renglones de agentes que no verifica nadie. No hay red de contención: si decís que un agente corre, corrilo.

**5. Ningún commit ni push por iniciativa propia.** Requiere instrucción explícita del PM en ese momento, aunque ya lo haya pedido antes en la sesión.

---

## Dónde está cada cosa

| Qué | Dónde |
|---|---|
| **Los 21 agentes ejecutables** | [`agents/`](agents/) · índice y convención en [`agents/README.md`](agents/README.md) |
| **El catálogo** — ~118 entradas por framework y por industria | [`README.md`](README.md) |
| **El curso de CrewAI + MCP** — 3 lecciones | [`crewai_mcp_course/`](crewai_mcp_course/) |
| **La SPA del atlas** — React 18 + Vite 6, desplegada a GitHub Pages | [`web/`](web/) · ⚠️ sin documentar, ver hallazgo 6 del diagnóstico |
| **CI** — 6 workflows | [`.github/workflows/`](.github/workflows/) |
| **Cómo contribuir** | [`CONTRIBUTION.md`](CONTRIBUTION.md) · [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) |
| **Política de seguridad** | [`SECURITY.md`](SECURITY.md) · ⚠️ contiene una afirmación falsa, ver regla 1 |
| **Estado de la adopción** — qué se midió y qué falta | [`docs/adopcion_ingenieria.md`](docs/adopcion_ingenieria.md) |
| **Reglas de desarrollo** — stack, arquitectura, DoD | [`docs/reglas/reglas_desarrollo.md`](docs/reglas/reglas_desarrollo.md) |
| **Cómo se despliega el catálogo web** | [`docs/manuales/manual_despliegue.md`](docs/manuales/manual_despliegue.md) |
| **Algo falló, qué hago** | [`docs/manuales/manual_resolucion_problemas.md`](docs/manuales/manual_resolucion_problemas.md) |
| **Modelo de amenaza y registro de riesgos** | `docs/riesgos.md` · 🚧 lo crea el paso 8 |

---

## Reglas de ingeniería

El manual de ingeniería es **central**: no vive en este repositorio, se consume desde afuera. Hay dos vías de acceso, y conviene saber cuál estás usando:

- **A. El plugin de Claude Code** — `ingenieria@etmunoz`, que expone la skill `ingenieria` y los comandos `/ingenieria:*`. Es la vía normal cuando se trabaja con Claude Code. Se instala con `claude plugin marketplace add etmunoz/ingenieria` y `claude plugin install ingenieria@etmunoz`. **No se actualiza solo, y hacen falta dos comandos**: `claude plugin marketplace update etmunoz` trae la revisión nueva, y `claude plugin update ingenieria@etmunoz` mueve tu instalación a ella. Si corrés solo el primero, no cambia nada y ningún comando avisa.
- **B. Una copia sincronizada** de los capítulos dentro del proyecto, para leerlos sin Claude Code, sin red, o desde otra herramienta. Este proyecto **no la tiene**: usa la vía A.

**El límite, en las dos direcciones:**

- Las reglas propias de este proyecto —qué framework usa cada agente, cómo se nombran las carpetas, la convención de `metadata.yaml`— **no van al manual central**, porque no le sirven a ningún otro proyecto. Van a `docs/reglas/reglas_desarrollo.md`.
- Y al revés: **una corrección hecha sobre una copia local del manual se pierde en la próxima sincronización**. Si encontrás algo equivocado o incompleto en el manual, se corrige en el repositorio central (`etmunoz/ingenieria`), que es donde lo heredan todos los proyectos.
