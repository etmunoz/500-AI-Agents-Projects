# Auditoría de código — 2026-09-11

**Proyecto:** `etmunoz/500-AI-Agents-Projects`
**Audiencia:** el PM, para decidir qué atacar primero.
**Contesta:** ¿qué hay en este repositorio que convenga tocar, y con cuánta confianza lo sabemos?
**Alcance:** los 27 `.py` y 37 `.md` versionados. `web/` **no** se analizó — ver *Lo que no se miró*.

> **Auditar no es reparar.** Este documento es un reporte, no un commit. **No se borró ni se editó una sola línea de código** al producirlo. Si algo de acá amerita limpieza, va en un plan aparte con sus propias pruebas y con la confirmación explícita de que no tiene dependientes reales.

---

## Calibración — por qué la primera corrida no servía

| Corrida | Objetos | Aristas | Hallazgos |
|---|---|---|---|
| Sin configuración | 191 | 1193 | **35** |
| Calibrada | **192** | **1204** | **11** |

De 35 hallazgos, **34 eran falsos positivos**. Lo único que se declaró fueron los **26 puntos de entrada**: cada `agent.py` se ejecuta con `uv run python agent.py` desde su carpeta y nadie lo importa, porque la autocontención es el diseño declarado en las reglas §2.1. Sin declararlos, los 24 aparecían como "módulos huérfanos".

**No se bajó ningún umbral ni se estrechó el alcance.** La prueba está en la primera columna: los objetos **subieron** de 191 a 192 y las aristas de 1193 a 1204. Una calibración que reduce hallazgos reduciendo lo que se mira es un falso verde; ésta mira más y reporta menos.

### El conteo es plausible, verificado contra la realidad

Antes de creerle a ningún número se comprobó que la herramienta estuviera mirando de verdad:

| Lo que la herramienta contó | Lo que hay en el repositorio | |
|---|---|---|
| 27 módulos | 27 archivos `.py` versionados | ✅ exacto |
| 37 documentos | 37 archivos `.md` versionados | ✅ exacto |
| 94 funciones + 33 constantes | 104 `def`/`class` de nivel superior | ✅ plausible |

Cero sobre nada no es cero. Acá no es cero, y además el denominador cierra.

---

## Hallazgos

**11 en total: 1 real, 10 falsos positivos confirmados.**

### Rompe algo si se toca mal

Ninguno.

### Código muerto real

| # | Objeto | Confianza | Qué es |
|---|---|---|---|
| **1** | `agents/13-customer-support-agent/agent.py::route_after_escalation_check` (línea 98) | **alta** | Router que nunca se cableó |

```python
def route_after_escalation_check(state: SupportState) -> Literal["generate", "generate"]:
    return "generate"
```

**Confianza alta porque se verificó buscando en todo el repositorio:** `grep -n 'route_after_escalation_check'` devuelve **una sola línea** — su propia definición. No hay registro por decorador, ni invocación por cadena, ni mención en ningún documento.

**Lo que lo hace interesante no es que esté muerta, sino lo que delata.** La anotación de retorno dice `Literal["generate", "generate"]`: **el mismo destino repetido dos veces**. Alguien escribió un router para bifurcar entre dos caminos, terminó con uno solo, y el grafo quedó con `add_edge("check_escalation", "generate")` —una arista incondicional— en vez de `add_conditional_edges`.

**El agente funciona igual.** La bandera `escalate` sí cambia el comportamiento: entra en el prompt (línea 80) y se muestra como `[ESCALATED]` (línea 159). Lo que no ocurre es el ruteo. Borrar esta función no cambia nada — pero mientras esté, cualquiera que lea el archivo va a creer que hay una bifurcación que no existe, en un ejemplo didáctico cuyo nombre es *"routes complex issues to human escalation"*.

**Destino sugerido:** borrarla, o cablearla de verdad con los dos destinos que la anotación insinúa. Las dos son defendibles; la decisión es del PM. **No se tocó.**

### Falsos positivos confirmados

| # | Hallazgos | Qué son | Verificación |
|---|---|---|---|
| 2–10 | 9 × `funcion_muerta` | **Invocación por framework.** 3 funciones en `mcp_server.py` decoradas con `@mcp.tool()`, y 6 métodos `_run` de subclases de `BaseTool` de CrewAI | Se leyó el decorador y la clase base de cada una |
| 11 | 1 × `ref_rota` | **Defecto de la herramienta.** Reporta que `README.md` enlaza a `.github/workflows/star-history.yml` "que no existe". El archivo existe y el enlace es correcto | `referencias_cruzadas.py:176` salta **toda carpeta que empiece con punto**, así que nunca indexó `.github/`. Cualquier enlace a una carpeta oculta se reporta roto |

Los 9 primeros son el falso positivo que el paso 7 nombra primero: *"las herramientas marcan como sin uso prácticamente todo handler registrado por decorador porque no ven la llamada directa"*. No se corrigen bajando umbrales.

---

## Lo que no se miró, y hay que decirlo

- **`web/` no se analizó.** Son 1.579 líneas de React —`App.jsx` sola tiene 1.057, por encima del umbral de deuda técnica de las reglas §4.4—. `front_dirs` quedó vacío **a propósito y declarado** en la configuración, en vez de omitido: la herramienta no tiene analizador para este stack. **El archivo más grande del repositorio está fuera de esta auditoría.**
- **`.github/` no se indexó**, por el defecto de la herramienta descrito arriba. Los 6 workflows quedaron fuera del grafo.
- **No se corrió `auditoria_superficies.py`.** Requiere `auditoria_superficies.toml` con las excepciones del proyecto —qué endpoints son públicos a propósito, qué pantallas ve cada rol— y este repositorio **no tiene endpoints ni roles**: no hay backend, no hay autenticación. Correrla sería medir una superficie que no existe.
- **No se creó `docs/referencias/mapa.yaml`.** Un mapa del sistema contesta *"si cambio X, ¿qué más tengo que tocar?"*, y acá la respuesta es estructuralmente **"nada"**: los 21 agentes son autocontenidos por diseño y no se importan entre sí. Las 1.204 aristas del grafo ya generado cubren lo que un mapa aportaría. Se declara como no aplicable, no como pendiente.
- **Esto es análisis estático.** No prueba que ningún agente funcione. Sigue habiendo **cero pruebas** en el repositorio.

---

## Resumen por confianza y severidad

| Severidad | Alta confianza | Media/posible | Falsos positivos |
|---|---|---|---|
| Rompe algo si se toca mal | 0 | 0 | — |
| Código muerto real | **1** | 0 | 9 |
| Duplicación | 0 | 0 | 0 |
| Convención cosmética | 0 | 0 | 1 |

**Un hallazgo real, de severidad baja.** No se inventaron hallazgos para tener algo que mostrar.

---

## Para el manual central (se propone en el paso 9)

**`referencias_cruzadas.py` reporta como enlace roto cualquier referencia a una carpeta que empiece con punto.** La línea 176 salta esos directorios al recorrer el árbol, así que su contenido nunca entra al índice — y después, cualquier documento que los enlace parece apuntar a la nada. En un repositorio con GitHub Actions eso es garantizado: `.github/workflows/` es exactamente el tipo de ruta que un README enlaza. El hallazgo se ve idéntico a uno real.

**Y la herramienta se cae si `--salida-dir` apunta fuera del repositorio.** `referencias_cruzadas.py:1339` hace `p.relative_to(raiz)` para imprimir la ruta y lanza `ValueError` — después de haber terminado el análisis y escrito los archivos. Importa porque el paso 0 del manual **instruye a usar `--salida-dir` con una carpeta temporal fuera del repositorio** para no ensuciarlo.
