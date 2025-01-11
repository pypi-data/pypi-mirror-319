from typing import Self


class DynareError(Exception):
    """Exception raised for errors occurring during the execution of the dynare Julia command."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"DynareError: {self.message}"

    @classmethod
    def from_julia_error(cls, julia_error) -> Self:
        message = f"JuliaError:\n{str(julia_error)}"
        return cls(message)
