# Manual de resolución de problemas — `500-AI-Agents-Projects`

**Proyecto:** `etmunoz/500-AI-Agents-Projects`
**Audiencia:** quien clonó el repositorio y algo no funciona — un agente que no arranca, un hook que no frena, un sitio que sale en blanco.
**Contesta:** algo falló, ¿qué hago?
**Fecha de creación:** 2026-09-11
**Última actualización:** 2026-09-11 — creación

---

## Antes de leer

Cada entrada tiene **síntoma → causa → qué hacer**. Buscá por el síntoma, que es lo único que tenés cuando llegás acá.

Casi todas estas trampas se midieron durante la adopción del manual de ingeniería, en esta misma máquina, entre el 2026-09-11 y ese mismo día. No son hipótesis: son cosas que ya pasaron.

**Lo que NO está en este manual:**

- Cómo publicar el sitio → [`manual_despliegue.md`](manual_despliegue.md)
- Las reglas que gobiernan el código → [`docs/reglas/reglas_desarrollo.md`](../reglas/reglas_desarrollo.md)
- Qué hace cada agente → el `README.md` de ese agente

**La regla que se aplica antes que cualquier entrada:** si un chequeo no pudo correr, la respuesta es **NO SÉ**, nunca verde. Un verde que no dice sobre qué es una afirmación que la corrida no respalda.

---

## Agentes

### El agente arranca y muere pidiendo una clave

**Síntoma:** error de autenticación de OpenAI, o `None` donde debía ir la clave.

**Causa:** falta el `.env`, o está pero vacío. **Es el primer arranque esperado**, no una falla del agente.

**Qué hacer:** desde la carpeta del agente,

```bash
cp .env.example .env
```

y poné la clave adentro. `.env.example` lista exactamente qué variables necesita ese agente — no son las mismas para todos: el 01 necesita también `TAVILY_API_KEY`, el 06 `NEWS_API_KEY`, el 07 `GITHUB_TOKEN`.

### `ModuleNotFoundError` con un paquete que jurás haber instalado

**Síntoma:** `No module named 'langchain'` justo después de un `pip install` exitoso.

**Causa:** casi siempre, el `venv` equivocado. **Cada agente tiene el suyo**: este repositorio no es un monorepo y no hay entorno compartido (reglas §2.1). Instalar en la carpeta del agente 01 no sirve para el 02.

**Qué hacer:** verificá dónde estás parado y qué intérprete está activo.

```bash
pwd                       # tiene que ser la carpeta del agente
python -c "import sys; print(sys.prefix)"
```

Si `sys.prefix` no apunta al `.venv` de **esa** carpeta, activá el correcto antes de diagnosticar nada más.

### Un agente que funcionaba dejó de funcionar sin que nadie lo tocara

**Síntoma:** errores de importación o de firma dentro del framework, no en el código del agente.

**Causa:** el framework sacó una versión nueva. Los manifiestos fijan con `==` justamente para esto, pero **20 de 22 lo hacen**: los dos del agente 21 usan `>=` y quedan expuestos.

**Qué hacer:** reinstalá desde el manifiesto en un entorno limpio. Si el agente usa `>=` y el problema es ese, fijá la versión que funciona y proponelo como PR.

### El agente 15 me dejó archivos `test_*.py` sueltos

**Síntoma:** archivos `test_algo.py` sin rastrear después de correr el generador de pruebas.

**Causa:** es lo que hace ese agente: escribe las pruebas que genera en la carpeta desde donde se lo ejecuta.

**Qué hacer:** borralos a mano. **No están en `.gitignore` a propósito**: el patrón escondería las pruebas reales el día que el repositorio tenga alguna, y hoy no tiene ninguna.

---

## Git y hooks

### El hook de secretos no frena nada

**Síntoma:** commiteás algo con una clave y pasa sin decir nada.

**Causa, en orden de frecuencia:**

1. **Los hooks no están activados en este clon.** `core.hooksPath` vive en `.git/config`, que **no se versiona**: clonar no lo trae.
2. **Docker está apagado.** Es el motor que efectivamente corre hoy.
3. **Los hooks perdieron el bit de ejecución.** En Linux y macOS git omite un hook no ejecutable **en silencio**.

**Qué hacer:**

```bash
git config core.hooksPath .githooks     # 1 — una vez por clon
docker info                             # 2 — tiene que responder
git ls-files -s .githooks/              # 3 — pre-commit y pre-push deben decir 100755
```

Y después **probalo intentando commitear un secreto inventado**, no leyendo el archivo. Un hook de seguridad se verifica ejecutándolo: la primera versión de este se escribió, se instaló y commiteó el secreto sin chistar, tres veces, y las tres el archivo se veía correcto.

### El pre-commit dice "NO se revisaron secretos"

**Síntoma:** `Ningún motor disponible: NO se revisaron secretos.`

**Causa:** ni Docker ni Python disponibles. **Esto es un "no sé", no un verde**, y el commit pasa igual — un hook que bloquea todo commit en una máquina a la que le falta una herramienta se desinstala el mismo día.

**Qué hacer:** levantá Docker. Si preferís el motor en Python y no está en el PATH:

```bash
git config --local ingenieria.python /ruta/al/python
```

### `bad interpreter` al correr un hook, en Linux o macOS

**Síntoma:** `/bin/sh^M: bad interpreter: No such file or directory`.

**Causa:** el hook llegó con fines de línea CRLF. Git para Windows trae `core.autocrlf=true` **a nivel sistema**.

**Qué hacer:** no debería pasar — [`.gitattributes`](../../.gitattributes) fuerza `eol=lf` en `.githooks/*` y `*.sh`. Si pasa, ese archivo se perdió o el hook llegó por fuera de git. Verificá:

```bash
file .githooks/pre-commit      # debe decir "POSIX shell script", sin "CRLF"
```

> En Windows esto **no** falla: MSYS tolera el `\r`. Por eso es peligroso — en la máquina donde se escribe el hook, parece que funciona.

### Git avisa que va a convertir LF a CRLF

**Síntoma:** `warning: in the working copy of 'X', LF will be replaced by CRLF`.

**Causa:** `core.autocrlf=true` a nivel sistema, en Windows.

**Qué hacer:** **nada.** Es normal y está gobernado por `.gitattributes`, que fija qué se guarda en el repositorio. Lo que git almacena sigue siendo LF.

### Un push se rechaza por falta de `Signed-off-by`

**Síntoma:** el workflow DCO falla con `N of M commit(s) missing a valid Signed-off-by line`.

**Causa:** la línea tiene que coincidir **exactamente** con el autor del commit, nombre y correo.

**Qué hacer:**

```bash
git rebase --signoff origin/main
git push --force-with-lease
```

Para los próximos, `git commit -s` la agrega sola.

---

## Python en Windows

### `python` está en el PATH pero no existe

**Síntoma:** ejecutar `python` abre la Microsoft Store, o imprime *"no se encontró Python"*. Y sin embargo `command -v python` lo encuentra.

**Causa:** Windows instala alias de la Microsoft Store en `WindowsApps` que **están en el PATH y fallan al ejecutarse**. Toda herramienta que pregunte "¿está instalado?" con `command -v` los da por buenos.

**Qué hacer:** instalá Python de verdad. Para comprobar si un intérprete sirve, **probalo**, no preguntes si está:

```bash
python -c ""     # silencio y código 0 = funciona
```

Si no queda en el PATH, declaralo para los hooks de este clon:

```bash
git config --local ingenieria.python "/c/ruta/al/python.exe"
```

### El pre-push dice `NO SÉ` en "agentes (sintaxis)"

**Síntoma:** la comprobación no sale verde ni roja.

**Causa:** no hay Python utilizable. La comprobación sale con código **2**, que significa *no pude medir*.

**Qué hacer:** instalá Python. **No es un fallo y no frena el push** — pero tampoco es un verde, y el hook lo dice en pantalla precisamente para que no se lea como uno.

---

## Sitio del catálogo

### La página publicada sale en blanco

**Síntoma:** el HTML carga, no hay contenido, y la consola del navegador muestra 404 en los assets.

**Causa:** el `base` de [`web/vite.config.js`](../../web/vite.config.js) está fijo en `/500-AI-Agents-Projects/`. Si el repositorio se llama distinto, las rutas no resuelven.

**Qué hacer:** ajustá `base` al nombre real del repositorio y reconstruí.

### El workflow construye bien y falla al desplegar

**Síntoma:** los pasos de build en verde, y el último rojo con un error de permisos sobre `github-pages`.

**Causa:** Pages no está habilitado en el repositorio.

**Qué hacer:** **Settings → Pages → Source: GitHub Actions**. Detalle en [`manual_despliegue.md`](manual_despliegue.md).

### Un enlace funciona en `npm run dev` y da 404 publicado

**Causa:** `dev` sirve desde la raíz y no aplica el `base` de producción.

**Qué hacer:** verificá con `npm --prefix web run preview`, que sí lo usa, antes de dar por bueno un cambio de rutas.

### El despliegue parece colgado

**Causa:** `concurrency: pages` con `cancel-in-progress: false`. Dos pushes seguidos a `main` se encolan; el segundo espera.

**Qué hacer:** mirá si hay otro despliegue corriendo **antes** de cancelar.

---

## Límites conocidos

- **Este manual cubre lo que ya falló, no todo lo que puede fallar.** Las entradas salen de problemas medidos durante la adopción. Un síntoma que no está acá no significa que no exista.
- **Las entradas de agentes se verificaron por lectura del código, no ejecutándolos.** Esta máquina no tiene Python: ningún agente se corrió para confirmar el síntoma exacto ni el texto literal del error.
- **No hay diagnóstico automático.** No existe un comando de "revisá mi instalación" que verifique hooks, entorno y dependencias de una vez. Todo lo de acá es manual.
- **Nada cubre fallas de los proveedores externos** —OpenAI, Tavily, NewsAPI, GitHub, TrustBoost— más allá de que el agente debería mostrar el error con su causa. Que un proveedor esté caído es un caso de prueba que todavía no existe (reglas, anexo E).

---

## Dónde sigue esto

| Si tu pregunta es… | Andá a |
|---|---|
| ¿Cómo publico el sitio? | [`manual_despliegue.md`](manual_despliegue.md) |
| ¿Cuáles son las reglas del repositorio? | [`docs/reglas/reglas_desarrollo.md`](../reglas/reglas_desarrollo.md) — §11.2 tiene las trampas con su mecanismo |
| ¿Qué es esto y cómo empiezo? | [`README.md`](../../README.md) |
| ¿Cómo contribuyo? | [`CONTRIBUTION.md`](../../CONTRIBUTION.md) |
| ¿Qué puede salir mal y qué sigue abierto? | 🚧 `manual_riesgos.md` — lo escribe el paso 8 de la adopción |
