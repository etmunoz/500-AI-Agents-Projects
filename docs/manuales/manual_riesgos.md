# Manual de riesgos — `500-AI-Agents-Projects`

**Proyecto:** `etmunoz/500-AI-Agents-Projects`
**Audiencia:** el PM y quien mantiene el repositorio, para saber qué está abierto y qué se cerró con evidencia.
**Contesta:** ¿qué puede salir mal, qué se hizo, y qué sigue abierto?
**Fecha de creación:** 2026-09-11
**Última actualización:** 2026-09-11 — creación

---

## Antes de leer

**Acá sólo entran riesgos observados, no riesgos imaginables.** Un registro lleno de amenazas abstractas entrena a ignorarlo. Cada uno de los que siguen se midió en este repositorio, con el comando o el ensayo al lado.

Dos reglas que lo mantienen honesto:

- **Un riesgo pasa a `mitigado` cuando existe evidencia de la verificación**, no cuando se escribió el arreglo. Marcar una casilla es afirmar un hecho.
- **Un riesgo `aceptado` lleva quién lo aceptó y cuándo.** La decisión es del PM, pero tiene nombre.

**Lo que NO está acá:** el modelo de amenaza y el inventario de superficie → [`manual_seguridad.md`](manual_seguridad.md).

---

## Resumen

| Estado | Cantidad |
|---|---|
| 🔴 Abierto | 5 |
| 🟢 Mitigado | 5 |
| 🟡 Aceptado | 2 |
| ⚫ Cerrado | 0 |

---

## Abiertos

### R-01 · Un aporte malicioso se ejecuta en la máquina de quien clona

- **Impacto:** alto. Un `agent.py` aceptado en un PR corre con los permisos de quien lo lanza: puede leer su `.env`, escribir en su disco y salir a la red. El alcance no es una máquina, sino todas las que clonen después.
- **Probabilidad:** baja hoy, creciente con la visibilidad del repositorio.
- **Estado:** 🔴 **abierto.** El único control es la revisión manual del PR. No hay análisis estático de seguridad, ni sandbox, ni CI que ejecute nada. **Un hook local no ayuda acá**: corre en la máquina de quien commitea, no en la nuestra.
- **Qué lo reduciría:** `bandit` bloqueante en CI, y un chequeo que marque red o disco no declarados en el README del agente.

### R-02 · Nada verifica el comportamiento de los 27 archivos Python

- **Impacto:** alto, y **ya se materializó dos veces**. Al no ejecutarse nunca, el repositorio acumuló: un manifiesto insatisfacible en el agente de referencia —que nadie podía instalar— y 23 archivos que morían en el primer `print` en una consola Windows. Los dos llevaban ahí desde antes del fork.
- **Probabilidad:** certeza. Ya pasó.
- **Estado:** 🔴 **abierto.** 0 archivos de prueba; ningún workflow ejecuta Python. El `pre-push` local comprueba **sintaxis**, que es el estado 1 de 3: no dice nada del comportamiento.
- **Qué lo reduciría:** un workflow que instale cada agente en un entorno limpio; una prueba por agente que confirme el fallo claro cuando falta la clave.
- **Verificado:** `git ls-files | grep -cE 'test|spec'` → 0 archivos de prueba, sobre 148 versionados.

### R-03 · Una dependencia comprometida corre en la máquina de quien instala

- **Impacto:** alto. 104 pines de PyPI en 24 manifiestos, más el árbol de npm de `web/`.
- **Probabilidad:** baja.
- **Estado:** 🔴 **abierto.** No se verifican firmas ni hashes. `pip-audit` y `npm audit` no corren en ningún lado. Lo único hecho fue comprobar **una vez, a mano**, que cada pin exista en PyPI — eso detecta manifiestos rotos, no paquetes maliciosos.
- **Mitigación parcial:** `web/package-lock.json` versionado y `npm ci` en el despliegue fijan **qué** se instala, no que sea benigno.

### R-04 · 17 de 21 agentes consumen la salida del modelo sin validarla

- **Impacto:** medio. Una salida fuera de formato cae en un camino no previsto. En material didáctico el daño extra es que **enseña el patrón equivocado** a quien copia el ejemplo.
- **Probabilidad:** media. Los modelos incumplen formato de forma intermitente.
- **Estado:** 🔴 **abierto** como deuda declarada. El criterio ya rige para lo que entre de ahora en adelante (reglas, anexo E).
- **Verificado:** 4 de 21 usan Pydantic, `with_structured_output` o `json.loads` con manejo de error.

### R-05 · Datos personales viajan a terceros sin control técnico

- **Impacto:** medio-alto según el dato. El agente 09 manda currículums a OpenAI; el 21 manda texto con PII a `api.trustboost.dev`.
- **Probabilidad:** certeza — es el propósito declarado de ambos.
- **Estado:** 🔴 **abierto.** Está documentado en las reglas §9 y en el README de cada agente, pero **ningún control técnico** impide que alguien meta un CV real como archivo de ejemplo.
- **Qué lo reduciría:** un chequeo que marque archivos con forma de dato personal real en los ejemplos.

---

## Mitigados

### R-06 · Una clave de API entra al historial

- **Impacto:** alto. Un secreto en el historial hay que rotarlo aunque se borre después: git no olvida y el repositorio puede haberse clonado en el medio.
- **Estado:** 🟢 **mitigado.** `.gitignore` cubre `.env` conservando `.env.example`; el `pre-commit` corre `gitleaks` y `revisar_secretos.py`.
- **Cómo se verificó:** se intentó commitear una clave **inventada** — no una de ejemplo de proveedor, que los escáneres ignoran. **Los dos motores la frenaron.** Además, barrido de `git log --all -p` contra patrones de OpenAI, GitHub, AWS, Google, Slack y PEM: **cero claves reales en toda la historia**.
- **Fecha:** 2026-09-11.
- **Residual:** si Docker está apagado y no hay Python declarado, el hook responde "no sé" y **deja pasar**. Y no protege de un PR ajeno.

### R-07 · Los hooks no corren fuera de Windows

- **Impacto:** alto y silencioso. Git **omite sin avisar** un hook no ejecutable, así que el repositorio quedaba sin protección de secretos en Linux y macOS mientras en Windows parecía funcionar.
- **Estado:** 🟢 **mitigado.** `core.filemode=false` en Git para Windows había hecho que el `chmod +x` no llegara al índice; se fijaron los modos con `git update-index --chmod=+x`.
- **Cómo se verificó:** `git ls-files -s .githooks/` **en un clon limpio** — no leyendo el índice local. Devuelve `100755` para `pre-commit` y `pre-push`.
- **Fecha:** 2026-09-11.

### R-08 · Un hook con CRLF falla con `bad interpreter`

- **Impacto:** alto y silencioso, por la misma razón que R-07.
- **Estado:** 🟢 **mitigado.** `.gitattributes` con `eol=lf` explícito en `.githooks/*` y `*.sh`. `core.autocrlf` está en `true` a nivel **sistema** en Git para Windows, así que sin esto cada clon decidía solo.
- **Cómo se verificó:** `file .githooks/pre-commit` → "POSIX shell script", sin CRLF. `git add --renormalize .` no cambia ningún archivo existente.
- **Fecha:** 2026-09-11.

### R-09 · La documentación afirmaba una protección que no existía

- **Impacto:** alto de una forma indirecta: `SECURITY.md` decía que los `.env` estaban "gitignored by default" y **no había ningún `.gitignore`**. Peor que omitir la protección — quien lo leía dejaba de revisar.
- **Estado:** 🟢 **mitigado.** El `.gitignore` existe, así que la afirmación pasó a ser cierta; y el texto se reescribió para aclarar que el hook **sólo protege un clon donde fue activado**.
- **Cómo se verificó:** `git check-ignore` sobre `.env`, `.env.local` y `.env.example` — los dos primeros ignorados, el tercero versionable.
- **Fecha:** 2026-09-11.

### R-10 · Los reportes de seguridad iban a un tercero no involucrado

- **Impacto:** alto. `SECURITY.md` y `CODE_OF_CONDUCT.md` dirigían vulnerabilidades y denuncias de conducta al correo del mantenedor del repositorio original, ajeno a este fork. Un reporte responsable terminaba en una bandeja que no puede actuar sobre él.
- **Estado:** 🟢 **mitigado.** Las 13 referencias al upstream reescritas o retiradas. Los reportes de seguridad van por el advisory privado de GitHub de **este** repositorio.
- **Cómo se verificó:** `grep -rnE 'ashishpatel26|ashishpatel\.ce\.2011'` sobre `.md` y `.yml` no devuelve nada fuera de `docs/`, donde son registro histórico.
- **Fecha:** 2026-09-11.
- **Residual:** el correo del upstream se **retiró** en vez de reemplazarse. Este proyecto todavía no publica una dirección directa — decisión pendiente del PM.

---

## Aceptados

### R-11 · Las acciones de GitHub están fijadas por etiqueta, no por hash

- **Impacto:** alto si se materializa. Una etiqueta mayor puede reapuntarse a otro commit, y esas acciones corren con `pages: write` e `id-token: write`.
- **Probabilidad:** muy baja. Son acciones oficiales de GitHub.
- **Estado:** 🟡 **aceptado.** Fijar por hash obliga a actualizar a mano en cada revisión de seguridad de las acciones, y el costo supera al beneficio para un repositorio sin datos de usuarios ni secretos de despliegue.
- **Aceptado por:** el PM, 2026-09-11.
- **Revisar si:** el repositorio pasa a manejar secretos en CI.

### R-12 · Un `.venv` no declarado puede ocultar código en el escaneo de secretos

- **Impacto:** bajo. `.gitignore` excluye `.venv/`, así que su contenido nunca llega al índice y el `pre-commit` sólo mira lo preparado.
- **Probabilidad:** baja.
- **Estado:** 🟡 **aceptado.** Es el comportamiento deseado: el escáner mira lo que se va a commitear, no el disco.
- **Aceptado por:** el PM, 2026-09-11.

---

## Dónde sigue esto

| Si tu pregunta es… | Andá a |
|---|---|
| ¿Qué se protege y de quién? | [`manual_seguridad.md`](manual_seguridad.md) |
| ¿Qué está medido y qué falta en el proyecto? | [`docs/adopcion_ingenieria.md`](../adopcion_ingenieria.md) |
| ¿Hacia dónde va el proyecto? | [`docs/roadmap.md`](../roadmap.md) |
| Algo falló, ¿qué hago? | [`manual_resolucion_problemas.md`](manual_resolucion_problemas.md) |
