# Hoja de ruta — `500-AI-Agents-Projects`

**Última revisión:** 2026-09-11 · **Audiencia:** quien decide en qué trabajar a continuación.

Esto es la visión compartida de hacia dónde va este repositorio. No es un cronograma ni un compromiso: es lo que se quiere que llegue a ser, con el motivo y quién lo pidió, para que un plan no tenga que salir de la nada.

**Las dos fronteras que la mantienen útil:**

- Si ya está **decidido, dimensionado y con fecha**, no es hoja de ruta: es un plan.
- Si está **roto**, no es hoja de ruta: es un riesgo o un pendiente. Los defectos medidos viven en [`docs/adopcion_ingenieria.md`](adopcion_ingenieria.md), no acá. Una hoja de ruta llena de defectos es un rastreador de errores con peores herramientas.

## Cómo se usa

- **Entrar es barato:** tres líneas —qué, por qué, quién lo pidió— y la fecha.
- **Salir es estricto:** una entrada sale **convertida en un plan** (y queda enlazada acá, no borrada) o **descartada con motivo y fecha**. No hay una tercera.
- **Se revisa para sacar cosas**, no sólo para agregar.
- **Los horizontes no son fechas.**

> **Sobre el origen de esta hoja de ruta.** Se sembró el 2026-09-11, durante el paso 4 de la adopción. El repositorio no tenía ninguna, y tampoco tenía planes cerrados ni `TODO`/`FUTURE` en el código de donde extraerla — se verificó con `grep -rnE 'TODO|FIXME|FUTURE|XXX|HACK'` sobre todos los `.py`, `.js`, `.jsx` y `.mjs`: **cero resultados**. Todo lo que sigue salió de intenciones que **ya estaban escritas** en `CONTRIBUTION.md` y en el propio nombre del repositorio, pero que vivían donde nadie las iba a releer. Nada acá es una idea inventada durante la adopción.

---

## Próximo

### Cerrar la secuencia de adopción del manual de ingeniería

- **Qué:** terminar los pasos 5 a 9 (`readme-proyecto`, `manuales`, `auditoria`, `seguridad`, `cierre`).
- **Por qué:** los pasos 0 a 4 dejaron el repositorio con reglas y protecciones, pero con tres cosas todavía abiertas que se tocan entre sí: el `README.md` manda a clonar otro repositorio, no hay modelo de amenaza, y no hay manuales.
- **Quién lo pidió:** el PM, 2026-09-11.
- **Depende de:** nada. Es el trabajo en curso.

### Reescribir las 13 referencias al upstream

- **Qué:** apuntar a `etmunoz/` las 13 referencias a `ashishpatel26` que quedan en 6 archivos. El inventario línea por línea está en [`docs/adopcion_ingenieria.md`](adopcion_ingenieria.md).
- **Por qué:** hoy, quien sigue el Quick Start clona el repositorio de otra persona, y quien reporta una vulnerabilidad o una conducta la manda al correo de otra persona.
- **Quién lo pidió:** el PM, 2026-09-11, al decidir que el fork diverge.
- **Depende de:** nada. Sale en los pasos 5 (`README.md`) y 8 (el resto).

---

## Después

### Las cinco categorías de aporte que `CONTRIBUTION.md` promete y no existen

- **Qué:** `CONTRIBUTION.md` (líneas 14-18) invita a aportar cinco cosas: plantillas y *boilerplates* por tipo de agente, integraciones (entornos, simuladores, herramientas de observabilidad), herramientas compartidas (arneses de evaluación, métricas, suites de *benchmark*, cargadores de datasets), experimentos reproducibles y utilidades de visualización. **Ninguna de las cinco tiene hoy dónde vivir**: el repositorio sólo tiene `agents/` y `crewai_mcp_course/`.
- **Por qué:** es una promesa escrita a quien quiera contribuir. Hoy alguien que llega con un arnés de evaluación no sabe dónde ponerlo, y lo más probable es que no lo aporte. Decidir la estructura —o retirar la invitación— convierte una promesa muerta en una de dos cosas útiles.
- **Quién lo pidió:** está en `CONTRIBUTION.md` desde antes del fork; lo recuperó la adopción el 2026-09-11.
- **Depende de:** una decisión del PM sobre si el repositorio quiere crecer en esa dirección o quedarse en catálogo + agentes.

### Que el catálogo se acerque al número que promete el nombre

- **Qué:** el repositorio se llama `500-AI-Agents-Projects` y el título del `README.md` dice "500+ AI Agent Projects & Use Cases". El contenido real, medido el 2026-09-11: **~118 entradas de catálogo** (95 por framework, 28 por industria, menos las filas de encabezado) y **21 agentes ejecutables**. Alrededor de 139.
- **Por qué:** hoy el titular no coincide con el contenido, y eso tiene dos salidas posibles —crecer hasta el número, o cambiar el número—. Las dos son legítimas; lo que no se sostiene es la distancia sin decidir.
- **Quién lo pidió:** nadie explícitamente; lo hereda el nombre del repositorio. Lo levantó la adopción como hallazgo 5 el 2026-09-11.
- **Depende de:** una decisión del PM. Es de producto, no de ingeniería.

---

## Algún día

### Un arnés que verifique que los agentes siguen corriendo

- **Qué:** algo que, con claves de prueba o respuestas grabadas, confirme periódicamente que los 21 agentes todavía arrancan contra las versiones de framework que declaran.
- **Por qué:** un ejemplo didáctico que dejó de funcionar es peor que ningún ejemplo, y hoy nada lo detectaría: no hay pruebas y el CI no ejecuta Python. La deuda de pruebas está registrada como defecto en la adopción; **esto es distinto**, es la ambición de que el catálogo se mantenga vivo solo.
- **Quién lo pidió:** nadie todavía. Lo anotó la adopción el 2026-09-11 al medir que 20 de 21 agentes dependen de un proveedor externo y de una versión fijada de framework.
- **Depende de:** que exista primero una suite mínima (deuda, no hoja de ruta).

---

## Ya hecho

Nada todavía: esta hoja de ruta se creó el 2026-09-11. Las entradas salen de acá convertidas en planes y quedan enlazadas en esta tabla, no borradas — es la única forma de ver, más adelante, qué parte de lo que se quería llegó a existir.

| Entrada | Plan | Fecha |
|---|---|---|
| — | — | — |

## Descartado

Nada todavía. Descartar no es fracasar: una idea que ya no aplica y sigue en la lista le quita atención a las que sí, y escribir el motivo acá evita que alguien la vuelva a proponer dentro de un año sin conocerlo.

| Entrada | Motivo | Fecha |
|---|---|---|
| — | — | — |
