import subprocess
import logging
from juliacall import Main as jl
from .dynare import dynare


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("DynarePython")


def check_julia_and_dynare():
    # Check Julia
    julia_path = jl.seval("Sys.BINDIR")
    julia_project = jl.seval("Base.active_project()")
    logger.info(f"Using julia at: {julia_path}")

    # Installed packages
    logger.info("Project status:")
    jl.seval("import Pkg; Pkg.status()")


_has_run = False


def _run_once():
    global _has_run
    if not _has_run:
        check_julia_and_dynare()
        jl.seval("using Pkg")
        _has_run = True


_run_once()

__all__ = ["dynare"]