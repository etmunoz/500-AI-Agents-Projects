"""
Archivo: herramientas/seguridad/revisar_secretos.py
Objetivo: Revisar lo que está por commitearse y frenar el commit si trae un
          secreto, un archivo de entorno real o un documento RAT.
Autor: Ezequiel Muñoz Krsulovic
Fecha y hora de creación: 2026-09-02 12:10
Fecha y hora de última modificación: 2026-09-10 14:23
Proyecto: herramienta genérica del manual de ingeniería (etmunoz/ingenieria)
Entorno: Python 3.11+ (solo biblioteca estándar salvo que se indique)

POR QUÉ ESTE REVISOR EXISTE
----------------------------
`reglas_desarrollo.md` §7 lo dice sin rodeos: un escáner de secretos en CI
encuentra el secreto **cuando ya entró al historial**, y entonces hay que
rotarlo aunque el commit siguiente lo borre. El hook lo evita antes de que
exista el commit.

Revisa el CONTENIDO INDEXADO (`git diff --cached`), no el del disco. Es la
diferencia que importa: `git add archivo` y después editarlo deja en el disco
algo distinto de lo que se va a commitear, y revisar el disco daría luz verde a
lo que sí entra.

EL MODO DE FALLO ES EL FALSO POSITIVO
--------------------------------------
Un hook que frena commits legítimos se saltea con `--no-verify`, y las reglas
prohíben ese atajo (§11). Un hook que se saltea siempre es peor que ninguno,
porque además da la sensación de que algo vigila. Por eso los patrones son
angostos a propósito:

La primera versión de este archivo dio **20 falsos positivos sobre este mismo
repositorio** y ninguno era un secreto. Los patrones de ahora salen de haber
mirado esos veinte:

- **Se exige entropía.** Un secreto generado mezcla clases de carácter; un
  identificador no. `CAMBIO_CONTRASENA = "cambio_contrasena"` no es un secreto,
  y `AUTH_SECRET=solo-para-el-build` tampoco. Se admite aparte la cadena
  hexadecimal larga, que tiene sólo dos clases y sin embargo es la forma más
  común de un secreto generado.
- **Se exige que sea un literal**, no una expresión. `${JWT_SECRET_KEY:?...}`,
  `contrasena=datos.contrasena`, `getpass.getpass(...)` y la anotación de tipo
  `contrasena: Mapped[bool]` no asignan nada: leen de otro lado.
- **No se revisa el contenido de los `.example`.** Existen para llevar valores
  de mentira; revisarlos es garantizar el ruido.
- **No se busca la palabra «contraseña» ni «secreto» sueltas.** Este proyecto
  está escrito en español y las menciona en documentación, mensajes de error y
  nombres de campo por todos lados.
- **En `tests/` no se aplica la regla del literal.** Una contraseña en una
  prueba es, por construcción, un valor de prueba. Las reglas de clave privada
  y de clave de AWS sí se aplican también ahí.

QUÉ FRENA
---------
1. Un `.env` real. `.env.example` y `.env.produccion.example` pasan: existen
   justamente para versionarse.
2. Cualquier archivo bajo `data/rat/`. Esos PDF dicen qué datos personales trata
   la organización y en qué sistemas, y el repositorio está en GitHub.
3. Bloques de clave privada.
4. Claves de acceso de AWS.
5. Asignaciones de un nombre sensible a un literal largo.

Se ejecuta solo, desde el hook. A mano:

    uv run python utilidades/hooks/revisar_secretos.py
    uv run python utilidades/hooks/revisar_secretos.py --todo   # el árbol entero

Devuelve 0 si está limpio, 1 si encontró algo.
"""

import argparse
import re
import subprocess  # nosec B404
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# DOS raices distintas, y confundirlas fue el defecto R-01
# ---------------------------------------------------------------------------
# `DIR_HERRAMIENTAS` es donde vive ESTE codigo: sale de __file__ y asi esta
# bien. `RAIZ` es el PROYECTO sobre el que se opera y NO sale de __file__: se
# fija en main() con `resolver_raiz`. El valor inicial es solo para importar.
DIR_HERRAMIENTAS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIR_HERRAMIENTAS))

from comun.raiz import resolver_raiz  # noqa: E402

RAIZ = Path.cwd()

for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8")

# Rutas que no se versionan nunca, aunque `.gitignore` fallara. El hook es la
# segunda barrera: el 2026-09-02 un patrón de `.gitignore` sin anclar ya se probó
# capaz de decidir sola qué entra y qué no, en la dirección contraria.
RUTAS_PROHIBIDAS = (
    # `data/` ENTERO, no sólo `data/rat/`. Ahí viven los insumos que describen
    # qué datos personales trata la organización y en qué sistemas: los RAT, y
    # desde el 2026-09-02 también la matriz de conexiones de Shopify, que trae
    # los Client ID de cada app instalada. `.gitignore` ya excluye `data/`; esto
    # es la segunda barrera.
    re.compile(r"(^|/)data/"),
    re.compile(r"(^|/)\.env$"),
    re.compile(r"(^|/)\.env\.(?!example$)(?!.*\.example$)"),
)

# Un secreto de verdad tiene entropía. Un identificador, un nombre de enum o un
# marcador de plantilla, no. Esta es la distinción que hace usable al hook: sin
# ella dio 20 falsos positivos sobre este mismo repositorio -- `CAMBIO_CONTRASENA
# = "cambio_contrasena"`, `contrasena=datos.contrasena`, `${JWT_SECRET_KEY:?...}`
# y los `.env.example` enteros. Un hook que frena eso se saltea con
# `--no-verify`, y las reglas prohíben ese atajo.
#
# `_` y `-` NO cuentan como símbolo: son los separadores de cualquier
# identificador, y contarlos volvería «sospechoso» a todo nombre en snake_case.
SIMBOLOS = re.compile(r"[^A-Za-z0-9_-]")
SOLO_HEX = re.compile(r"^[0-9a-fA-F]{32,}$")

# El valor no es un literal, sino una expresión: una interpolación de shell o
# compose (`${...}`), un atributo (`datos.contrasena`), una llamada
# (`getpass.getpass(...)`) o una anotación de tipo (`contrasena: Mapped[bool]`,
# que en Python usa el mismo `:` que un par clave-valor de YAML).
NO_ES_LITERAL = re.compile(r"[$(\[\]<>]|\.[A-Za-z_]|\?\.")

NOMBRE_SENSIBLE = (
    r"(secret[_-]?key|jwt[_-]?secret|auth[_-]?secret|api[_-]?key|access[_-]?token"
    r"|refresh[_-]?token|client[_-]?secret|private[_-]?key|password|passwd|contrasena)"
)

ASIGNACION = re.compile(
    NOMBRE_SENSIBLE + r"""\s*[:=]\s*["']?([^\s"',;]{12,})["']?""",
    re.IGNORECASE,
)

# Un literal de contraseña en una prueba es, por construcción, un valor de
# prueba: la suite lo usa para crear el usuario que la propia suite consulta.
# Las reglas de clave privada y de clave de AWS sí se aplican también acá.
RUTAS_SIN_REGLA_DE_LITERAL = re.compile(r"(^|/)tests?/")


def _tiene_entropia(valor: str) -> bool:
    """
    Objetivo: Decir si un literal se parece a un secreto y no a un identificador.
    Entrada: valor (str).
    Salida: bool.

    Se exigen tres clases de carácter (minúscula, mayúscula, dígito, símbolo), o
    bien una cadena hexadecimal larga -- que tiene sólo dos clases y sin embargo
    es la forma más común de un secreto generado.
    """
    if SOLO_HEX.match(valor):
        return True
    clases = sum(
        (
            any(c.islower() for c in valor),
            any(c.isupper() for c in valor),
            any(c.isdigit() for c in valor),
            bool(SIMBOLOS.search(valor)),
        )
    )
    return clases >= 3


CLAVE_PRIVADA = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
CLAVE_AWS = re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")

# Una línea puede eximirse explícitamente. Es la válvula que evita el
# `--no-verify`: quien sabe por qué su línea es legítima lo deja escrito en el
# código, donde el siguiente lo puede leer y discutir.
EXENTA = re.compile(r"#\s*permitido-secreto|//\s*permitido-secreto")


def _git(*argumentos: str) -> str:
    """
    Objetivo: Correr git y devolver su salida.
    Entrada: argumentos (str) del comando.
    Salida: str con la salida estándar, vacía si git falló.
    """
    try:
        # Lista fija de argumentos, sin shell.
        salida = subprocess.run(  # nosec B603
            ["git", *argumentos],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return salida.stdout if salida.returncode == 0 else ""


def revisar_ruta(ruta: str) -> str | None:
    """
    Objetivo: Decir si una ruta no debe versionarse nunca.
    Entrada: ruta (str) relativa a la raíz, con barras normales.
    Salida: str con el motivo, o None si la ruta está bien.
    """
    normalizada = ruta.replace("\\", "/")
    if normalizada.endswith(".example"):
        return None
    for patron in RUTAS_PROHIBIDAS:
        if patron.search(normalizada):
            if "data/" in normalizada:
                return "insumo de `data/`: describe qué datos personales trata la organización"
            return "archivo de entorno real: lleva claves, no plantillas"
    return None


def revisar_linea(linea: str, ruta: str = "") -> str | None:
    """
    Objetivo: Decir si una línea de contenido trae un secreto.
    Entrada: linea (str), sin el prefijo `+` del diff; ruta (str) del archivo.
    Salida: str con el motivo, o None si la línea está bien.
    """
    if EXENTA.search(linea):
        return None
    if CLAVE_PRIVADA.search(linea):
        return "bloque de clave privada"
    if CLAVE_AWS.search(linea):
        return "clave de acceso de AWS"

    normalizada = ruta.replace("\\", "/")
    if RUTAS_SIN_REGLA_DE_LITERAL.search(normalizada):
        return None

    asignacion = ASIGNACION.search(linea)
    if asignacion is None:
        return None
    valor = asignacion.group(2)
    if NO_ES_LITERAL.search(valor) or not _tiene_entropia(valor):
        return None
    return f"«{asignacion.group(1)}» asignado a un literal de {len(valor)} caracteres"


def _archivos_indexados() -> list[str]:
    """
    Objetivo: Listar las rutas que entran en este commit.
    Entrada: —
    Salida: list[str].

    `--diff-filter=d` deja fuera los borrados: una ruta que se está eliminando no
    puede filtrar nada.
    """
    salida = _git("diff", "--cached", "--name-only", "--diff-filter=d")
    return [r for r in salida.splitlines() if r.strip()]


def _lineas_agregadas(ruta: str) -> list[tuple[int, str]]:
    """
    Objetivo: Devolver las líneas que este commit AGREGA a un archivo.
    Entrada: ruta (str).
    Salida: list[tuple[int, str]] -- número de línea y contenido.

    Sólo lo agregado: un secreto que ya estaba en el historial no se arregla
    frenando este commit, y frenarlo dejaría el repositorio sin poder commitear
    nada hasta rotarlo. Eso se resuelve rotando la credencial, no acá.
    """
    diff = _git("diff", "--cached", "--unified=0", "--", ruta)
    lineas: list[tuple[int, str]] = []
    numero = 0
    for linea in diff.splitlines():
        if linea.startswith("@@"):
            cabecera = re.search(r"\+(\d+)", linea)
            numero = int(cabecera.group(1)) if cabecera else 0
            continue
        if linea.startswith("+++"):
            continue
        if linea.startswith("+"):
            lineas.append((numero, linea[1:]))
            numero += 1
    return lineas


def main() -> int:
    """
    Objetivo: Punto de entrada.
    Entrada: argumentos de línea de comandos.
    Salida: int -- 0 limpio, 1 si encontró algo.
    """
    analizador = argparse.ArgumentParser(description="Frena el commit si lo indexado trae un secreto.")
    analizador.add_argument(
        "--todo",
        action="store_true",
        help="revisar el árbol versionado entero, no sólo lo indexado",
    )
    analizador.add_argument("--raiz", default=None, help="raiz del proyecto sobre el que operar (por defecto, el repositorio git del directorio actual)")
    args = analizador.parse_args()

    global RAIZ
    RAIZ = resolver_raiz(args.raiz)

    hallazgos: list[str] = []

    if args.todo:
        rutas = [r for r in _git("ls-files").splitlines() if r.strip()]
    else:
        rutas = _archivos_indexados()

    for ruta in rutas:
        motivo = revisar_ruta(ruta)
        if motivo is not None:
            hallazgos.append(f"  {ruta}\n      {motivo}")
            continue

        # Un `.example` existe justamente para llevar valores de mentira. Revisar
        # su contenido es garantizar el falso positivo.
        if ruta.endswith(".example"):
            continue

        if args.todo:
            archivo = RAIZ / ruta
            try:
                contenido = archivo.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lineas = list(enumerate(contenido.splitlines(), start=1))
        else:
            lineas = _lineas_agregadas(ruta)

        for numero, texto in lineas:
            motivo = revisar_linea(texto, ruta)
            if motivo is not None:
                hallazgos.append(f"  {ruta}:{numero}\n      {motivo}")

    if not hallazgos:
        return 0

    print("COMMIT FRENADO -- posible secreto:\n", file=sys.stderr)
    for hallazgo in hallazgos:
        print(hallazgo, file=sys.stderr)
    print(
        "\nUn secreto que entra al historial hay que rotarlo aunque el commit\n"
        "siguiente lo borre. Por eso se frena acá y no en el pipeline.\n"
        "\n"
        "Si la línea es legítima, dejalo escrito en el código con el comentario\n"
        "`permitido-secreto` y volvé a commitear. NO uses `--no-verify`: las\n"
        "reglas lo prohíben (§11), y así el motivo queda donde el próximo lo lee.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
