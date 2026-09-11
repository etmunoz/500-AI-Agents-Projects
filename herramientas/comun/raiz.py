"""
Archivo: herramientas/comun/raiz.py
Objetivo: Resolver la raiz del PROYECTO sobre el que opera una herramienta,
          que no es la raiz de las herramientas.
Autor: Ezequiel Munoz
Fecha y hora de creación: 2026-09-10 19:45
Fecha y hora de última modificación: 2026-09-10 14:23
Proyecto: herramienta generica del manual de ingenieria (etmunoz/ingenieria)
Entorno: Python 3.11+ (solo biblioteca estandar)

Por que existe este modulo y no una copia en cada herramienta
-------------------------------------------------------------
Porque la copia YA fallo dos veces, y de la misma forma.

Toda herramienta de este repositorio maneja **dos raices distintas**, y
confundirlas fue el riesgo R-01:

- **Donde vive el codigo** (`DIR_HERRAMIENTAS`). Sale de `__file__`, y esta
  bien que salga de ahi: sirve para importar un modulo hermano o para leer
  otra herramienta.
- **El proyecto sobre el que se opera** (`RAIZ`). **No puede salir de
  `__file__`.** Si sale, la herramienta invocada desde otro proyecto opera
  sobre ESTE repositorio: audita el equivocado, escribe en el equivocado, o
  --lo peor-- escanea el equivocado y da verde sobre el del usuario.

En el proyecto de origen los scripts vivian en `scripts/`, un nivel bajo la
raiz, asi que `Path(__file__).parents[1]` daba la raiz de verdad. Aca viven
dos niveles adentro, y da `herramientas/`. **La forma llego copiada de un
lugar donde era correcta**, y por eso se corrige teniendo un solo lugar donde
esta escrita en vez de N copias que se ven bien cada una por su lado.

Como se usa
-----------
    DIR_HERRAMIENTAS = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(DIR_HERRAMIENTAS))
    from comun.raiz import resolver_raiz
    ...
    RAIZ = resolver_raiz(args.raiz)
"""

from __future__ import annotations

import subprocess  # nosec B404
from pathlib import Path


def resolver_raiz(arg: str | None = None) -> Path:
    """
    Objetivo: Resolver la raiz del PROYECTO sobre el que se opera.
    Entrada: arg (str|None) - valor de `--raiz`, si se paso.
    Salida: Path absoluto.
    Errores: Ninguno. Siempre devuelve algo; el peor caso es el directorio
             actual, que es donde la persona esta parada.

    Orden, y el motivo de cada escalon:

    1. **Lo declarado gana.** Si alguien paso `--raiz`, sabe algo que la
       herramienta no.
    2. **Despues git**, que acierta aunque se invoque desde una subcarpeta del
       proyecto -- el caso comun y el que `cwd` sola resuelve mal.
    3. **Por ultimo el directorio actual**, para que la herramienta siga
       sirviendo fuera de un repositorio git.

    Lo que NO esta en la lista es `__file__`, y esa ausencia es el arreglo.
    """
    if arg:
        return Path(arg).resolve()
    try:
        salida = subprocess.run(  # noqa: S603
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if salida:
            return Path(salida).resolve()
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.cwd().resolve()
