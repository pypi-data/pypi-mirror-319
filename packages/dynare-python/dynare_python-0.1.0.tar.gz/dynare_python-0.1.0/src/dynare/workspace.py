from dataclasses import dataclass, field
from typing import List, Any, Dict, Tuple, Union, Self, NamedTuple
import numpy as np


@dataclass
class PyIndices:
    current: List[int]
    forward: List[int]
    purely_forward: List[int]
    backward: List[int]
    both: List[int]
    non_backward: List[int]
    static: List[int]
    dynamic: List[int]
    dynamic_current: List[int]
    current_in_dynamic: List[int]
    forward_in_dynamic: List[int]
    backward_in_dynamic: List[int]
    current_in_dynamic_jacobian: List[int]
    current_in_static_jacobian: List[int]
    exogenous: List[int]
    n_endogenous: int
    D_columns: NamedTuple
    E_columns: NamedTuple
    UD_columns: List[int]
    UE_columns: List[int]

    @classmethod
    def from_julia(cls, julia_indices) -> Self:
        return cls(
            current=list(julia_indices.current),
            forward=list(julia_indices.forward),
            purely_forward=list(julia_indices.purely_forward),
            backward=list(julia_indices.backward),
            both=list(julia_indices.both),
            non_backward=list(julia_indices.non_backward),
            static=list(julia_indices.static),
            dynamic=list(julia_indices.dynamic),
            dynamic_current=list(julia_indices.dynamic_current),
            current_in_dynamic=list(julia_indices.current_in_dynamic),
            forward_in_dynamic=list(julia_indices.forward_in_dynamic),
            backward_in_dynamic=list(julia_indices.backward_in_dynamic),
            current_in_dynamic_jacobian=list(julia_indices.current_in_dynamic_jacobian),
            current_in_static_jacobian=list(julia_indices.current_in_static_jacobian),
            exogenous=list(julia_indices.exogenous),
            n_endogenous=julia_indices.n_endogenous,
            D_columns={
                "D": list(julia_indices.D_columns.D),
                "jacobian": list(julia_indices.D_columns.jacobian),
            },
            E_columns={
                "E": list(julia_indices.E_columns.E),
                "jacobian": list(julia_indices.E_columns.jacobian),
            },
            UD_columns=list(julia_indices.UD_columns),
            UE_columns=list(julia_indices.UE_columns),
        )


@dataclass
class PyCyclicReductionOptions:
    maxiter: int = 100
    tol: float = 1e-8

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(maxiter=julia_obj.maxiter, tol=julia_obj.tol)


@dataclass
class PyGeneralizedSchurOptions:
    criterium: float = 1.0 + 1e-6

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(criterium=julia_obj.criterium)


@dataclass
class PyLinearRationalExpectationsOptions:
    cyclic_reduction: PyCyclicReductionOptions = PyCyclicReductionOptions()
    generalized_schur: PyGeneralizedSchurOptions = PyGeneralizedSchurOptions()

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            cyclic_reduction=PyCyclicReductionOptions.from_julia(
                julia_obj.cyclic_reduction
            ),
            generalized_schur=PyGeneralizedSchurOptions.from_julia(
                julia_obj.generalized_schur
            ),
        )


@dataclass
class PySchurWs:
    work: List[float]
    wr: List[float]
    wi: List[float]
    vs: np.ndarray
    sdim: int
    bwork: List[int]
    eigen_values: List[complex]

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            work=list(julia_obj.work),
            wr=list(julia_obj.wr),
            wi=list(julia_obj.wi),
            vs=julia_obj.vs.to_numpy(),
            sdim=julia_obj.sdim,
            bwork=list(julia_obj.bwork),
            eigen_values=list(julia_obj.eigen_values),
        )


@dataclass
class PyLSEWs:
    work: List[complex]
    X: List[complex]

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), X=julia_obj.X.to_numpy())


@dataclass
class PyEigenWs:
    work: List[complex]
    rwork: List[float]
    VL: np.ndarray
    VR: np.ndarray
    W: List[complex]
    scale: List[float]
    iwork: List[int]
    rconde: List[float]
    rcondv: List[float]

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            work=list(julia_obj.work),
            rwork=list(julia_obj.rwork),
            VL=julia_obj.VL.to_numpy(),
            VR=julia_obj.VR.to_numpy(),
            W=list(julia_obj.W),
            scale=list(julia_obj.scale),
            iwork=list(julia_obj.iwork),
            rconde=list(julia_obj.rconde),
            rcondv=list(julia_obj.rcondv),
        )


@dataclass
class PyHermitianEigenWs:
    work: List[complex]
    rwork: List[float]
    iwork: List[int]
    w: List[complex]
    Z: np.ndarray
    isuppz: List

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            work=list(julia_obj.work),
            rwork=list(julia_obj.rwork),
            iwork=list(julia_obj.iwork),
            w=list(julia_obj.w),
            Z=julia_obj.Z.to_numpy(),
            isuppz=list(julia_obj.isuppz),
        )


@dataclass
class PyLUWs:
    ipiv: List(int)

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(ipiv=julia_obj.ipiv.to_numpy())


@dataclass
class PyQRWs:
    work: np.ndarray
    τ: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), τ=julia_obj.τ.to_numpy())


@dataclass
class PyQRWYWs:
    work: np.ndarray
    T: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), T=julia_obj.T.to_numpy())


@dataclass
class PyQRPivotedWs:
    work: np.ndarray
    rwork: np.ndarray
    τ: np.ndarray
    jpvt: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            work=julia_obj.work.to_numpy(),
            rwork=julia_obj.rwork.to_numpy(),
            τ=julia_obj.τ.to_numpy(),
            jpvt=julia_obj.jpvt.to_numpy(),
        )


@dataclass
class PyQROrmWs:
    work: np.ndarray
    τ: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), τ=julia_obj.τ.to_numpy())


@dataclass
class PyLyapdWs:
    AA: np.ndarray
    AAtemp: np.ndarray
    AA2: np.ndarray
    AA2temp: np.ndarray
    BB: np.ndarray
    temp1: np.ndarray
    XX: np.ndarray
    nonstationary_variables: List[bool]
    nonstationary_trends: List[bool]
    dgees_ws: "PySchurWs"
    linsolve_ws1: "PyLUWs"
    linsolve_ws2: "PyLUWs"

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            AA=julia_obj.AA.to_numpy(),
            AAtemp=julia_obj.AAtemp.to_numpy(),
            AA2=julia_obj.AA2.to_numpy(),
            AA2temp=julia_obj.AA2temp.to_numpy(),
            BB=julia_obj.BB.to_numpy(),
            temp1=julia_obj.temp1.to_numpy(),
            XX=julia_obj.XX.to_numpy(),
            nonstationary_variables=julia_obj.nonstationary_variables,
            nonstationary_trends=julia_obj.nonstationary_trends,
            dgees_ws=PySchurWs.from_julia(julia_obj.dgees_ws),
            linsolve_ws1=PyLUWs.from_julia(julia_obj.linsolve_ws1),
            linsolve_ws2=PyLUWs.from_julia(julia_obj.linsolve_ws2),
        )


@dataclass
class PyNonstationaryVarianceWs:
    rΣ_s_s: np.ndarray
    rA1: np.ndarray
    rA2: np.ndarray
    rB1: np.ndarray
    rB2: np.ndarray
    rA2S: np.ndarray
    rB2S: np.ndarray
    rΣ_ns_s: np.ndarray
    rΣ_ns_ns: np.ndarray
    state_stationary_variables: List[bool]
    nonstate_stationary_variables: List[bool]

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            rΣ_s_s=julia_obj.rΣ_s_s.to_numpy(),
            rA1=julia_obj.rA1.to_numpy(),
            rA2=julia_obj.rA2.to_numpy(),
            rB1=julia_obj.rB1.to_numpy(),
            rB2=julia_obj.rB2.to_numpy(),
            rA2S=julia_obj.rA2S.to_numpy(),
            rB2S=julia_obj.rB2S.to_numpy(),
            rΣ_ns_s=julia_obj.rΣ_ns_s.to_numpy(),
            rΣ_ns_ns=julia_obj.rΣ_ns_ns.to_numpy(),
            state_stationary_variables=julia_obj.state_stationary_variables,
            nonstate_stationary_variables=julia_obj.nonstate_stationary_variables,
        )


@dataclass
class PyVarianceWs:
    B1S: np.ndarray
    B1SB1: np.ndarray
    A2S: np.ndarray
    B2S: np.ndarray
    Σ_s_s: np.ndarray
    Σ_ns_s: np.ndarray
    Σ_ns_ns: np.ndarray
    stationary_variables: List[bool]
    nonstationary_ws: List[PyNonstationaryVarianceWs]
    lre_ws: PyLinearRationalExpectationsWs
    lyapd_ws: PyLyapdWs

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            B1S=julia_obj.B1S.to_numpy(),
            B1SB1=julia_obj.B1SB1.to_numpy(),
            A2S=julia_obj.A2S.to_numpy(),
            B2S=julia_obj.B2S.to_numpy(),
            Σ_s_s=julia_obj.Σ_s_s.to_numpy(),
            Σ_ns_s=julia_obj.Σ_ns_s.to_numpy(),
            Σ_ns_ns=julia_obj.Σ_ns_ns.to_numpy(),
            stationary_variables=julia_obj.stationary_variables,
            nonstationary_ws=[
                PyNonstationaryVarianceWs.from_julia(ns)
                for ns in julia_obj.nonstationary_ws
            ],
            lre_ws=PyLinearRationalExpectationsWs.from_julia(julia_obj.lre_ws),
            lyapd_ws=PyLyapdWs.from_julia(julia_obj.lyapd_ws),
        )


@dataclass
class PyBunchKaufmanWs:
    work: np.ndarray
    ipiv: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), ipiv=julia_obj.ipiv.to_numpy())


@dataclass
class PyCholeskyPivotedWs:
    work: np.ndarray
    piv: np.ndarray

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(work=julia_obj.work.to_numpy(), piv=julia_obj.piv.to_numpy())


@dataclass
class PyGsSolverWs:
    tmp1: np.ndarray
    tmp2: np.ndarray
    g1: np.ndarray
    g2: np.ndarray
    luws1: PyLUWs
    luws2: PyLUWs
    schurws: PyGeneralizedSchurWs

    @classmethod
    def from_julia(cls, d, n1):
        n = d.shape[0]
        n2 = n - n1
        tmp1 = np.empty((n1, n1))  # Create similar matrix for tmp1
        tmp2 = np.empty((n1, n1))  # Create similar matrix for tmp2
        g1 = np.empty((n1, n1))  # Create similar matrix for g1
        g2 = np.empty((n2, n1))  # Create similar matrix for g2

        # Conversion of luws1 and luws2 using LUWs equivalents
        luws1 = PyLUWs(np.empty((n1, n1)))  # Example placeholder
        luws2 = PyLUWs(np.empty((n2, n2)))  # Example placeholder

        # Conversion of schurws using GeneralizedSchurWs equivalents
        schurws = PyGeneralizedSchurWs(d.to_numpy())  # Convert d to numpy array


@dataclass
class PyLinearGsSolverWs:
    solver_ws: "PyGsSolverWs"
    ids: PyIndices
    d: List[float]
    e: List[float]

    @classmethod
    def from_julia(cls, julia_solver_ws) -> "PyLinearGsSolverWs":
        return cls(
            solver_ws=PyGsSolverWs.from_julia(
                julia_solver_ws.solver_ws
            ),  # Assuming PyGsSolverWs is defined
            ids=PyIndices.from_julia(julia_solver_ws.ids),
            d=julia_solver_ws.d.to_numpy(),  # Convert Julia Matrix to NumPy array
            e=julia_solver_ws.e.to_numpy(),  # Convert Julia Matrix to NumPy array
        )


@dataclass
class PyLinearCyclicReductionWs:
    solver_ws: PyCyclicReductionWs
    ids: PyIndices
    a: List[float]
    b: List[float]
    c: List[float]
    x: List[float]

    @classmethod
    def from_julia(cls, julia_cyclic_ws) -> "PyLinearCyclicReductionWs":
        return cls(
            solver_ws=PyCyclicReductionWs.from_julia(
                julia_cyclic_ws.solver_ws
            ),  # Assuming PyCyclicReductionWs is defined
            ids=PyIndices.from_julia(julia_cyclic_ws.ids),
            a=julia_cyclic_ws.a.to_numpy(),
            b=julia_cyclic_ws.b.to_numpy(),
            c=julia_cyclic_ws.c.to_numpy(),
            x=julia_cyclic_ws.x.to_numpy(),
        )


@dataclass
class PyLinearRationalExpectationsWs:
    ids: PyIndices
    jacobian_static: List[float]
    qr_ws: "PyQRWs"
    ormqr_ws: "PyQROrmWs"
    solver_ws: Union["PyLinearGsSolverWs", "PyLinearCyclicReductionWs"]
    A_s: List[float]
    C_s: List[float]
    Gy_forward: List[float]
    Gy_dynamic: List[float]
    temp: List[float]
    AGplusB_backward: List[float]
    jacobian_forward: List[float]
    jacobian_current: List[float]
    b10: List[float]
    b11: List[float]
    AGplusB: List[float]
    linsolve_static_ws: "PyLUWs"
    AGplusB_linsolve_ws: "PyLUWs"

    @classmethod
    def from_julia(cls, julia_lre_ws) -> Self:
        solver_ws = (
            PyLinearGsSolverWs.from_julia(julia_lre_ws.solver_ws)
            if type(julia_lre_ws.solver_ws) == "LinearGsSolverWs"
            else PyLinearCyclicReductionWs.from_julia(julia_lre_ws.solver_ws)
        )

        return cls(
            ids=PyIndices.from_julia(julia_lre_ws.ids),
            jacobian_static=julia_lre_ws.jacobian_static.to_numpy(),
            qr_ws=PyQRWs.from_julia(julia_lre_ws.qr_ws),  # Assuming PyQRWs is defined
            ormqr_ws=PyQROrmWs.from_julia(
                julia_lre_ws.ormqr_ws
            ),  # Assuming PyQROrmWs is defined
            solver_ws=solver_ws,
            A_s=julia_lre_ws.A_s.to_numpy(),
            C_s=julia_lre_ws.C_s.to_numpy(),
            Gy_forward=julia_lre_ws.Gy_forward.to_numpy(),
            Gy_dynamic=julia_lre_ws.Gy_dynamic.to_numpy(),
            temp=julia_lre_ws.temp.to_numpy(),
            AGplusB_backward=julia_lre_ws.AGplusB_backward.to_numpy(),
            jacobian_forward=julia_lre_ws.jacobian_forward.to_numpy(),
            jacobian_current=julia_lre_ws.jacobian_current.to_numpy(),
            b10=julia_lre_ws.b10.to_numpy(),
            b11=julia_lre_ws.b11.to_numpy(),
            AGplusB=julia_lre_ws.AGplusB.to_numpy(),
            linsolve_static_ws=PyLUWs.from_julia(
                julia_lre_ws.linsolve_static_ws
            ),  # Assuming PyLUWs is defined
            AGplusB_linsolve_ws=PyLUWs.from_julia(
                julia_lre_ws.AGplusB_linsolve_ws
            ),  # Assuming PyLUWs is defined
        )
