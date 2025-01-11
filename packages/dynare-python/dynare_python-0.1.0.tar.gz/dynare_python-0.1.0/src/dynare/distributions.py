""" Python conversion of the base types from the Julia Distributions package. """

from abc import ABC, abstractmethod
from typing import Type, Any, Tuple, Union, Self
from math import prod

## VariateForm and its Subtypes


class VariateForm(ABC):
    """Specifies the form or shape of the variate or a sample."""

    pass


class ArrayLikeVariate(VariateForm):
    """Specifies the number of axes of a variate or a sample."""

    def __init__(self, n: int):
        self.n = n


class Univariate(ArrayLikeVariate):
    def __init__(self):
        super().__init__(0)


class Multivariate(ArrayLikeVariate):
    def __init__(self):
        super().__init__(1)


class Matrixvariate(ArrayLikeVariate):
    def __init__(self):
        super().__init__(2)


class CholeskyVariate(VariateForm):
    """Specifies that the variate or sample is of type Cholesky."""

    pass


## ValueSupport and its Subtypes


class ValueSupport(ABC):
    """Abstract type that specifies the support of elements of samples."""

    pass


class Discrete(ValueSupport):
    """Represents the support of a discrete random variable (countable)."""

    pass


class Continuous(ValueSupport):
    """Represents the support of a continuous random variable (uncountable)."""

    pass


# Promotion rule: Combination of Discrete and Continuous yields Continuous
def promote_rule(type1: Type[Continuous], type2: Type[Discrete]) -> Type[Continuous]:
    return Continuous


## Sampleable


class Sampleable(ABC):
    """Sampleable is any type able to produce random values."""

    def __init__(
        self, variate_form: Type[VariateForm], value_support: Type[ValueSupport]
    ):
        self.variate_form = variate_form
        self.value_support = value_support

    @abstractmethod
    def rand(self) -> Any:
        """Abstract method to generate a random sample."""
        pass


def variate_form(sampleable: Type[Sampleable]) -> Type[VariateForm]:
    return sampleable.variate_form


def value_support(sampleable: Type[Sampleable]) -> Type[ValueSupport]:
    return sampleable.value_support


# Define the size and length of Sampleable objects
def length(s: Sampleable) -> int:
    if isinstance(s.variate_form, Univariate):
        return 1
    elif isinstance(s.variate_form, Multivariate):
        raise NotImplementedError("Multivariate length is not implemented")
    else:
        return prod(size(s))


def size(s: Sampleable) -> Tuple:
    if isinstance(s.variate_form, Univariate):
        return ()
    elif isinstance(s.variate_form, Multivariate):
        return (length(s),)
    else:
        return tuple()


def eltype(sampleable: Type[Sampleable]) -> Type:
    if isinstance(sampleable.value_support, Discrete):
        return int
    elif isinstance(sampleable.value_support, Continuous):
        return float
    else:
        raise TypeError("Unknown value support type")


## nsamples


def nsamples(sampleable: Type[Sampleable], x: Any) -> int:
    if isinstance(sampleable.variate_form, Univariate):
        if isinstance(x, (int, float)):
            return 1
        elif isinstance(x, (list, tuple)):
            return len(x)
    elif isinstance(sampleable.variate_form, Multivariate):
        if isinstance(x, (list, tuple)):
            return 1
        elif isinstance(x, (list, tuple)) and isinstance(x[0], list):
            return len(x[0])
    raise TypeError(f"Unsupported type for nsamples: {type(x)}")


## Equality and Hashing for Sampleable objects


def sampleable_equal(s1: Sampleable, s2: Sampleable) -> bool:
    if s1.__class__.__name__ != s2.__class__.__name__:
        return False
    for f in vars(s1):
        if getattr(s1, f) != getattr(s2, f):
            return False
    return True


def sampleable_hash(s: Sampleable, h: int) -> int:
    hashed = hash(Sampleable)
    hashed = hash(s.__class__.__name__) + h
    for f in vars(s):
        hashed += hash(getattr(s, f))
    return hashed


## Distribution as a subtype of Sampleable


class Distribution(Sampleable):
    """Distribution is a Sampleable generating random values from a probability distribution."""

    def __init__(
        self, variate_form: Type[VariateForm], value_support: Type[ValueSupport]
    ):
        super().__init__(variate_form, value_support)

    @classmethod
    def convert_jl_distribution(cls, jl_distribution: Any) -> Self:
        return Distribution()


# Defining common distribution types
class UnivariateDistribution(Distribution):
    def __init__(self, value_support: Type[ValueSupport]):
        super().__init__(Univariate(), value_support)


class MultivariateDistribution(Distribution):
    def __init__(self, value_support: Type[ValueSupport]):
        super().__init__(Multivariate(), value_support)


class MatrixDistribution(Distribution):
    def __init__(self, value_support: Type[ValueSupport]):
        super().__init__(Matrixvariate(), value_support)


class DiscreteDistribution(Distribution):
    def __init__(self, variate_form: Type[VariateForm]):
        super().__init__(variate_form, Discrete)


class ContinuousDistribution(Distribution):
    def __init__(self, variate_form: Type[VariateForm]):
        super().__init__(variate_form, Continuous)
