# Overview

This Python package wraps the [Dynare.jl](https://github.com/DynareJulia/Dynare.jl) Julia package, which provides a Julia interface to the [Dynare](https://www.dynare.org/) software for economic modeling.

The package provides a `dynare(model_path: Path)` function which takes a path to a Dynare model file and returns a `Context` Python object, which is a Python equivalent of the `Dynare.Context` Julia object.

Julia `AxisArrayGrid` objects are converted to Pandas `DataFrame` objects, and Julia `Matrix` objects are converted to NumPy `ndarray` objects.

Under the hood, the project uses the [JuliaCall](https://juliapy.github.io/PythonCall.jl/stable/) library to call Julia code from Python and convert Julia objects to Python objects.

## Installation

The package can be installed from PyPI with the following command:

```bash
pip install dynare-python
```

### Quickstart

```python
from dynare import dynare

context = dynare("<path_to_model_file.mod>")
print(context)
```

## Examples

You can find example mod files in the `examples` folder of this repo.

## Configuration

To reuse and existing Julia environment, set the `PYTHON_JULIAPKG_EXE=<exe>` and `PYTHON_JULIAPKG_PROJECT=<project>` environment variables as documented in [pyjuliapkg](https://github.com/JuliaPy/PyJuliaPkg?tab=readme-ov-file#configuration).

### No X-Windows server

Dynare will try to open windows on your machine when it's completed computing. If there is no display on your system, you probably want to set the following environment variables to avoid related
error messages:

```
export QT_QPA_PLATFORM=offscreen
export DESKTOP_SESSION=none
```

