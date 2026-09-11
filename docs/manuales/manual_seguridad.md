# Manual de seguridad — `500-AI-Agents-Projects`

**Proyecto:** `etmunoz/500-AI-Agents-Projects`
**Audiencia:** quien decide si un aporte entra, y quien necesita saber qué se protege acá y cómo se verifica.
**Contesta:** ¿es seguro esto, y cómo lo sé?
**Fecha de creación:** 2026-09-11
**Última actualización:** 2026-09-11 — creación

---

## Antes de leer

**La superficie de este repositorio no es un servidor: es la máquina de otra gente.**

No hay backend, no hay autenticación, no hay endpoints, no hay datos de usuarios. Lo que sí hay es **código que se publica para que desconocidos lo ejecuten localmente**, con sus propias claves de API y su propio crédito. Todo lo que sigue parte de ahí, y es lo que hace que un pentest clásico no aplique y que la revisión de aportes sea el control principal.

**Lo que NO está en este manual:**

- Qué puede salir mal y en qué estado está → [`manual_riesgos.md`](manual_riesgos.md)
- Algo falló y querés el síntoma → [`manual_resolucion_problemas.md`](manual_resolucion_problemas.md)
- Cómo reportar una vulnerabilidad → [`SECURITY.md`](../../SECURITY.md)
- Las reglas que gobiernan el código → [`docs/reglas/reglas_desarrollo.md`](../reglas/reglas_desarrollo.md) §9

---

## 1. Modelo de amenaza

### Qué se protege

| Activo | Por qué importa |
|---|---|
| **La clave de API de quien clona** | Es el activo que más cerca está de perderse: 24 carpetas traen `.env.example` y el arranque documentado es copiarlo a `.env`. Un descuido lo publica en un repositorio público. |
| **La máquina de quien ejecuta un agente** | Un `agent.py` aportado por un tercero corre con los permisos de quien lo lanza. Puede leer, escribir y salir a la red. |
| **El crédito de API de quien ejecuta** | Un bucle sin corte gasta dinero ajeno. No es un daño teórico: es una factura. |
| **La integridad de lo que publicamos** | Si alguien inserta algo dañino en un ejemplo, lo ejecutan todos los que clonen después. El alcance es el de la audiencia del repositorio, no el de una máquina. |
| **Los datos personales que pasan por dos agentes** | El 09 procesa currículums y el 21 procesa PII, y los dos los mandan a terceros. |

### De quién

| Adversario | Qué podría hacer |
|---|---|
| **Un aporte malicioso** | Un PR con un `agent.py` que exfiltra el `.env` de quien lo corra, o descarga y ejecuta algo. **Es el adversario principal y el más realista.** |
| **Una dependencia comprometida** | 104 pines desde PyPI y el árbol de npm de `web/`. Una versión maliciosa corre en la máquina de quien instale. |
| **Un contribuyente descuidado** | No es un atacante, pero el resultado se parece: una clave real commiteada, un CV real como archivo de ejemplo. |
| **Un tercero al que los agentes le hablan** | OpenAI, Tavily, NewsAPI, GitHub, yfinance, TrustBoost. Una respuesta manipulada entra al contexto de un modelo que después decide cosas. |
| **Quien tome control de la cuenta de GitHub** | Podría publicar desde `main` directo a GitHub Pages, y alterar lo que se distribuye. |

### Qué se asume confiable, y por lo tanto no se prueba

**Esta es la parte que más suele fallar, y por eso se escribe.**

- **GitHub Actions y sus acciones de terceros** (`checkout@v4`, `setup-node@v4`, `configure-pages@v5`, `upload-pages-artifact@v3`, `deploy-pages@v4`, `github-script@v7`). Están fijadas por etiqueta mayor, **no por hash**: una etiqueta puede reapuntarse.
- **PyPI y npm** como distribuidores. No se verifican firmas ni hashes de los paquetes.
- **Los proveedores de modelos** cumplen su contrato y no devuelven algo diseñado para dañar a quien lo consuma.
- **La máquina de quien desarrolla** no está comprometida.
- **`gitleaks` y `revisar_secretos.py` detectan lo que dicen detectar.** Se probaron con claves inventadas, no con un conjunto exhaustivo.

---

## 2. Inventario de superficie

Sin inventario, "corrimos unas pruebas" no se convierte en "de N superficies, M están cubiertas".

| # | Superficie | Estado | Con qué |
|---|---|---|---|
| 1 | **Secretos entrando al historial** | ✅ `cubierta` | `.gitignore` + hook `pre-commit` con dos motores. **Verificado ejecutando**: una clave inventada fue frenada por ambos |
| 2 | **Código de terceros que se publica y otros ejecutan** | ⚠️ `solo_revision` | Revisión manual de cada PR. No hay análisis estático de seguridad, ni sandbox, ni CI que ejecute nada |
| 3 | **Dependencias de Python** (104 pines, 24 manifiestos) | ⚠️ `descubierta` | Nada las verifica. Se comprobó una vez, a mano, que cada pin exista en PyPI |
| 4 | **Dependencias de npm** de `web/` | ⚠️ `parcial` | `package-lock.json` versionado y `npm ci` en el despliegue: fija **qué** se instala, no que sea benigno |
| 5 | **Datos personales hacia terceros** (agentes 09 y 21) | ⚠️ `solo_documentada` | Declarado en las reglas §9 y en el README de cada agente. Ningún control técnico |
| 6 | **El pipeline de despliegue** | ✅ `cubierta` | Permisos mínimos (`contents: read`, `pages: write`, `id-token: write`); sin escritura al repositorio |
| 7 | **El sitio publicado** | ✅ `fuera_de_alcance` | Estático, sin backend, sin formularios, sin almacenamiento. No hay entrada de usuario que atacar. *Firmado: PM, 2026-09-11* |
| 8 | **Autenticación y autorización** | ✅ `fuera_de_alcance` | No existen. No hay cuentas, sesiones ni roles. *Firmado: PM, 2026-09-11* |
| 9 | **El servidor MCP del curso** (`lesson_03`) | ✅ `fuera_de_alcance` | Material didáctico que se levanta a mano en `localhost` y expone tres herramientas sin efectos. No se despliega. *Firmado: PM, 2026-09-11* |

**Cobertura medida: 4 de 9 superficies cubiertas o fuera de alcance con firma; 5 descubiertas o parciales.**

---

## 3. Por qué no hay arnés de pentest

**No se instaló `scripts/pentest_suite.py`, y no es un pendiente: no aplica.**

El arnés del manual central levanta la aplicación en una instancia desechable y ataca sus endpoints — autenticación, autorización, inyección, escalada de privilegios. Este repositorio **no tiene ninguna de esas cosas**: sin servidor, sin sesiones, sin roles, sin base de datos de usuarios, sin un solo endpoint HTTP propio. Copiar el arnés dejaría una lista de chequeos apuntando a rutas inexistentes, y **una lista mitad ruido enseña a ignorarla** — que es exactamente lo que el paso advierte.

**Lo que sí se hizo en su lugar**, porque es donde está la superficie real:

| Ejercicio | Resultado |
|---|---|
| Intentar commitear una clave inventada | **Frenado** por los dos motores. La clave se inventó a propósito: las de ejemplo de los proveedores están en las listas de excepción y el ensayo habría medido el señuelo |
| Verificar el bit de ejecución de los hooks en un clon limpio | `100755`. Antes era `100644`, y git omite un hook no ejecutable **en silencio** |
| Buscar ejecución dinámica en los 27 archivos Python | **Cero.** Ni `exec`, ni `eval`, ni `subprocess`, ni `os.system`, ni `PythonREPL`, ni `shell=True` |
| Buscar claves reales en el historial completo | **Cero.** `git log --all -p` contra patrones de OpenAI, GitHub, AWS, Google, Slack y PEM |
| Revisar los permisos del workflow de despliegue | Mínimos, sin escritura al repositorio |

> **Lo documentado como seguro se ejecuta igual.** Los cinco ejercicios se corrieron; ninguno se dio por bueno leyendo.

---

## 4. Componentes con modelo de lenguaje

20 de los 21 agentes llaman a un modelo. Los tres límites de confianza:

1. **La entrada del usuario no es confiable.** Llega por argumento de línea de comandos o por archivo.
2. **La salida del modelo no es confiable.** Es texto generado, no un contrato. **Medición al 2026-09-11: sólo 4 de 21 agentes la validan.** Los otros 17 la consumen tal cual — deuda declarada en las reglas, anexo E.
3. **Lo que devuelve un tercero no es confiable.** Resultados de búsqueda, artículos de noticias, issues de GitHub: todo eso entra al contexto de un modelo que después decide.

**El prompt de sistema se asume descubrible.** Ninguno lleva secretos ni credenciales. Verificado: ningún `agent.py` interpola una variable de entorno dentro de un prompt.

**La agencia se verifica, no se supone.** Lo que estos agentes pueden disparar es: llamadas HTTP a los proveedores declarados, lectura de archivos que se les pasan por argumento, y escritura de sus salidas en la carpeta desde donde se los ejecuta. **Ninguno ejecuta código generado por el modelo**, y esa propiedad se mantiene: agregar uno que lo haga requiere aprobación explícita y una capa de validación escrita en Python.

> El agente 08 tiene una bandera `--allow-dangerous-code` que habilita el intérprete de pandas de LangChain. Está **apagada por defecto** y hay que pedirla a mano, pero es la excepción a la frase anterior y por eso se nombra acá.

---

## Límites conocidos

- **No hay análisis estático de seguridad en CI.** Ni `bandit`, ni `pip-audit`, ni `npm audit` bloqueante, ni escaneo de secretos del lado del servidor. El único control es el hook local, **y un hook local no protege de un PR ajeno**: corre en la máquina de quien commitea, no en la nuestra.
- **La revisión manual es el único control sobre el aporte malicioso**, que es el adversario principal. No escala y no tiene red.
- **Las acciones de GitHub están fijadas por etiqueta, no por hash.** Una etiqueta mayor puede reapuntarse a otro commit.
- **Cero pruebas.** Ninguna afirmación de comportamiento de este manual está respaldada por una suite.
- **Los ejercicios cubren lo que se pensó probar.** No hubo revisión externa ni pentest de terceros.

---

## Dónde sigue esto

| Si tu pregunta es… | Andá a |
|---|---|
| ¿Qué puede salir mal, y en qué estado está? | [`manual_riesgos.md`](manual_riesgos.md) |
| Encontré una vulnerabilidad, ¿cómo la reporto? | [`SECURITY.md`](../../SECURITY.md) |
| Voy a aportar código, ¿qué se espera? | [`CONTRIBUTION.md`](../../CONTRIBUTION.md) |
| Algo falló y quiero el síntoma | [`manual_resolucion_problemas.md`](manual_resolucion_problemas.md) |
| ¿Cómo se despliega, y con qué permisos? | [`manual_despliegue.md`](manual_despliegue.md) |
