from pathlib import Path
from dynare import dynare


def test_dynare():
    print(dynare(Path(__file__).parent.parent / "examples" / "example1pf_bad.mod"))


if __name__ == "__main__":
    test_dynare()
