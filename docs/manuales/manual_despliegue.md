# Manual de despliegue — `500-AI-Agents-Projects`

**Proyecto:** `etmunoz/500-AI-Agents-Projects`
**Audiencia:** quien necesita publicar el catálogo web, o entender por qué una publicación falló o salió distinta a lo esperado.
**Contesta:** ¿cómo se pone el sitio del catálogo en producción desde cero, y qué lo rompe?
**Fecha de creación:** 2026-09-11
**Última actualización:** 2026-09-11 — lockfile versionado y workflow a `npm ci`

---

## Antes de leer

Lo único que este repositorio despliega es **`web/`**, la SPA del catálogo, a **GitHub Pages**. Los 21 agentes de `agents/` no se despliegan: se ejecutan en la máquina de quien los clona, y eso no es un despliegue sino un uso.

Al terminar esto vas a poder publicar el sitio desde un fork recién hecho, entender qué hace el workflow en cada paso, y reconocer las cuatro cosas que lo rompen.

**Lo que NO está en este manual:**

- Algo falló y querés el síntoma concreto → [`manual_resolucion_problemas.md`](manual_resolucion_problemas.md)
- Cómo se ejecuta un agente → el `README.md` de ese agente, en `agents/<NN>-<nombre>/`
- Por qué la arquitectura es así → [`docs/reglas/reglas_desarrollo.md`](../reglas/reglas_desarrollo.md) §3
- El modelo de amenaza del despliegue → [`manual_seguridad.md`](manual_seguridad.md)

---

## Qué se despliega, y qué lo dispara

| | |
|---|---|
| **Qué** | `web/dist/` — el resultado de `vite build` sobre `web/` |
| **A dónde** | GitHub Pages, entorno `github-pages` |
| **Quién lo hace** | [`.github/workflows/jekyll-gh-pages.yml`](../../.github/workflows/jekyll-gh-pages.yml) |
| **Cuándo** | En cada `push` a `main`. También a mano con `workflow_dispatch` |
| **En un PR** | El job `build` corre, el job `deploy` **no** (`if: github.event_name != 'pull_request'`). Un PR verifica que compile, no publica |

> El nombre del archivo dice `jekyll` por herencia del upstream. **No hay Jekyll acá**: es Vite. El nombre no se cambió para no romper referencias externas.

## Publicar desde un fork recién hecho

**El paso que no está automatizado y sin el cual todo lo demás falla: hay que habilitar Pages a mano.**

1. En el repositorio de GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

   Sin esto, el workflow corre, construye bien, y **falla recién en el último paso** con un error de permisos sobre el entorno `github-pages`. El build verde de los primeros pasos hace creer que el problema es de despliegue y no de configuración.

2. Verificar que el `base` de Vite coincida con el nombre del repositorio. En [`web/vite.config.js`](../../web/vite.config.js):

   ```js
   base: "/500-AI-Agents-Projects/",
   ```

   Es una ruta **fija**. Si el fork se llama distinto, el sitio carga el HTML pero **todos los assets dan 404**: la página aparece en blanco sin ningún error visible en la interfaz. Ver *Límites conocidos*.

3. Empujar a `main`, o disparar el workflow a mano desde la pestaña Actions.

4. La URL publicada queda en la salida del job `deploy`, y en **Settings → Pages**.

## Qué hace el workflow, paso por paso

| Paso | Qué hace | Qué mirar si falla |
|---|---|---|
| `actions/checkout@v4` | Clona el repositorio | — |
| `actions/setup-node@v4` | Node **22** | Localmente probado con Node 24. Si algo compila acá y no allá, empezar por esta diferencia |
| `actions/configure-pages@v5` | Prepara el entorno de Pages | Falla si Pages no está habilitado — ver el paso 1 de arriba |
| `npm ci` en `web/` | Instala exactamente lo que fija `package-lock.json` | Falla si el lockfile no coincide con `package.json` — commitealos juntos |
| `npm run build` en `web/` | `vite build` → `web/dist/` | Referencia local: 1674 módulos en 2,07 s (2026-09-11) |
| `upload-pages-artifact@v3` | Sube `web/dist` | — |
| `deploy-pages@v4` | Publica | Sólo fuera de un PR |

**Permisos que el workflow declara:** `contents: read`, `pages: write`, `id-token: write`. Son los mínimos para publicar; no tiene permiso de escritura sobre el repositorio.

**Concurrencia:** `group: "pages"` con `cancel-in-progress: false`. Dos pushes seguidos a `main` **no** se pisan: el segundo espera al primero. Si un despliegue parece colgado, mirá si hay otro corriendo antes de cancelarlo.

## Construir y previsualizar en local

```bash
npm --prefix web ci             # exactamente lo que fija el lockfile
npm --prefix web run build      # produce web/dist/
npm --prefix web run preview    # sirve web/dist/ como lo haría Pages
```

Para desarrollo con recarga en caliente, `npm --prefix web run dev`.

> `npm run dev` sirve desde la raíz y **no** respeta el `base` de producción. Un enlace que funciona en `dev` puede dar 404 publicado. Antes de dar por bueno un cambio de rutas, verificalo con `preview`, que sí usa el `base`.

## Revertir una publicación

No hay botón de revertir. El sitio publicado es siempre el resultado del último `main`:

```bash
git revert <commit-que-rompió>
git push
```

El workflow se dispara solo y republica. **No se edita `web/dist/` a mano**: es un artefacto derivado y la próxima publicación lo pisa.

---

## Límites conocidos

- ~~El despliegue no es reproducible.~~ **Resuelto el 2026-09-11.** `web/package-lock.json` está versionado y el workflow usa `npm ci`, que instala exactamente lo bloqueado y falla si el lockfile no coincide con `package.json`. Antes usaba `npm install` sin lockfile: con rangos `^` en [`web/package.json`](../../web/package.json), dos publicaciones del mismo commit podían embarcar versiones distintas sin que nada lo registrara. **Consecuencia práctica:** cambiar una dependencia ahora exige commitear el lockfile junto al `package.json`, o el despliegue falla — que es el punto.
- **El `base` de Vite está fijo al nombre del repositorio.** Un fork con otro nombre publica un sitio en blanco, sin error visible.
- **Las variables `VITE_*` se hornean en tiempo de build.** Cambiarlas en el entorno de Pages después de construir no tiene ningún efecto: hay que reconstruir. Hoy el proyecto no usa ninguna, pero es la trampa que aparece la primera vez que se agrega una.
- **Nada verifica que el sitio publicado sea correcto.** El workflow comprueba que *compile*, no que funcione: no hay prueba de humo, ni verificación de enlaces sobre el sitio construido, ni captura comparada. Un cambio que compila y rompe la navegación se publica sin resistencia.
- **No hay entorno de pruebas.** No existe un *staging*: de `main` se va directo a producción. El único ensayo previo posible es el job `build` de un PR, que sólo dice que compila.
- **No se probó un despliegue desde cero en un fork nuevo.** Los pasos de arriba salen de leer el workflow y la configuración de Vite, verificados contra el repositorio; la secuencia completa en un fork recién creado **no se ejecutó**. Es un manual verificado por lectura, no por corrida.

---

## Dónde sigue esto

| Si tu pregunta es… | Andá a |
|---|---|
| Algo falló y quiero el síntoma concreto | [`manual_resolucion_problemas.md`](manual_resolucion_problemas.md) |
| ¿Cómo está construido y por qué así? | [`docs/reglas/reglas_desarrollo.md`](../reglas/reglas_desarrollo.md) |
| ¿Qué es este repositorio y cómo empiezo? | [`README.md`](../../README.md) |
| ¿Qué puede salir mal y qué sigue abierto? | [`manual_riesgos.md`](manual_riesgos.md) |
| ¿Es seguro, y cómo se verifica? | [`manual_seguridad.md`](manual_seguridad.md) |
