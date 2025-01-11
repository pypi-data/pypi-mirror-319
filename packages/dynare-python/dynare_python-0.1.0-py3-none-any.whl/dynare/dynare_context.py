import logging
import ctypes
import os
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Any, Dict, Tuple, Union, Self, TypeVar, Generic
import numpy as np
import pandas as pd
import scipy.stats as stats


logger = logging.getLogger("dynare.dynare_context")


class SymbolType(Enum):
    Endogenous = 0
    Exogenous = 1
    ExogenousDeterministic = 2
    Parameter = 3
    DynareFunction = 4

    @classmethod
    def from_julia(cls, jl_symboltype) -> Self:
        return SymbolType(
            int(
                str(repr(jl_symboltype))
                .replace("Julia: Endogenous::SymbolType = ", "")
                .replace("Julia: Exogenous::SymbolType = ", "")
                .replace("Julia: ExogenousDeterministic::SymbolType = ", "")
                .replace("Julia: Parameter::SymbolType = ", "")
                .replace("Julia: DynareFunction::SymbolType = ", "")
            )
        )


class EstimatedParameterType(Enum):
    EstParameter = 0
    EstSDShock = 1
    EstSDMeasurement = 2
    EstVarShock = 3
    EstVarMeasurement = 4
    EstCorrShock = 5
    EstCorrMeasurement = 6

    @classmethod
    def from_julia(cls, jl_estimatedparametertype) -> Self:
        return EstimatedParameterType(
            int(
                str(repr(jl_estimatedparametertype))
                .replace("Julia: EstParameter::EstimatedParameterType = ", "")
                .replace("Julia: EstSDShock::EstimatedParameterType = ", "")
                .replace("Julia: EstSDMeasurement::EstimatedParameterType = ", "")
                .replace("Julia: EstVarShock::EstimatedParameterType = ", "")
                .replace("Julia: EstVarMeasurement::EstimatedParameterType = ", "")
                .replace("Julia: EstCorrShock::EstimatedParameterType = ", "")
                .replace("Julia: EstCorrMeasurement::EstimatedParameterType = ", "")
            )
        )


def get_member(obj, member, default=None):
    try:
        return getattr(obj, member)
    except AttributeError:
        return default


@dataclass
class ModFileInfo:
    endval_is_reset: bool = False
    has_auxiliary_variables: bool = False
    has_calib_smoother: bool = False
    has_check: bool = False
    has_deterministic_trend: bool = False
    has_dynamic_file: bool = False
    has_endval: bool = False
    has_histval: bool = False
    has_histval_file: bool = False
    has_initval: bool = False
    has_initval_file: bool = False
    has_planner_objective: bool = False
    has_perfect_foresight_setup: bool = False
    has_perfect_foresight_solver: bool = False
    has_ramsey_model: bool = False
    has_shocks: bool = False
    has_static_file: bool = False
    has_steadystate_file: bool = False
    has_stoch_simul: bool = False
    has_trends: bool = False
    initval_is_reset: bool = False
    modfilepath: str = ""

    def __repr__(self) -> str:
        return (
            f"ModFileInfo(\n"
            f"  endval_is_reset={self.endval_is_reset},\n"
            f"  has_auxiliary_variables={self.has_auxiliary_variables},\n"
            f"  has_calib_smoother={self.has_calib_smoother},\n"
            f"  has_check={self.has_check},\n"
            f"  has_deterministic_trend={self.has_deterministic_trend},\n"
            f"  has_dynamic_file={self.has_dynamic_file},\n"
            f"  has_endval={self.has_endval},\n"
            f"  has_histval={self.has_histval},\n"
            f"  has_histval_file={self.has_histval_file},\n"
            f"  has_initval={self.has_initval},\n"
            f"  has_initval_file={self.has_initval_file},\n"
            f"  has_planner_objective={self.has_planner_objective},\n"
            f"  has_perfect_foresight_setup={self.has_perfect_foresight_setup},\n"
            f"  has_perfect_foresight_solver={self.has_perfect_foresight_solver},\n"
            f"  has_ramsey_model={self.has_ramsey_model},\n"
            f"  has_shocks={self.has_shocks},\n"
            f"  has_static_file={self.has_static_file},\n"
            f"  has_steadystate_file={self.has_steadystate_file},\n"
            f"  has_stoch_simul={self.has_stoch_simul},\n"
            f"  has_trends={self.has_trends},\n"
            f"  initval_is_reset={self.initval_is_reset},\n"
            f"  modfilepath={self.modfilepath}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_modfileinfo) -> Self:
        return ModFileInfo(
            endval_is_reset=jl_modfileinfo.endval_is_reset,
            has_auxiliary_variables=jl_modfileinfo.has_auxiliary_variables,
            has_calib_smoother=jl_modfileinfo.has_calib_smoother,
            has_check=jl_modfileinfo.has_check,
            has_deterministic_trend=jl_modfileinfo.has_deterministic_trend,
            has_dynamic_file=jl_modfileinfo.has_dynamic_file,
            has_endval=jl_modfileinfo.has_endval,
            has_histval=jl_modfileinfo.has_histval,
            has_histval_file=jl_modfileinfo.has_histval_file,
            has_initval=jl_modfileinfo.has_initval,
            has_initval_file=jl_modfileinfo.has_initval_file,
            has_planner_objective=jl_modfileinfo.has_planner_objective,
            has_perfect_foresight_setup=jl_modfileinfo.has_perfect_foresight_setup,
            has_perfect_foresight_solver=jl_modfileinfo.has_perfect_foresight_solver,
            has_ramsey_model=jl_modfileinfo.has_ramsey_model,
            has_shocks=jl_modfileinfo.has_shocks,
            has_static_file=jl_modfileinfo.has_static_file,
            has_steadystate_file=jl_modfileinfo.has_steadystate_file,
            has_stoch_simul=jl_modfileinfo.has_stoch_simul,
            has_trends=jl_modfileinfo.has_trends,
            initval_is_reset=jl_modfileinfo.initval_is_reset,
            modfilepath=jl_modfileinfo.modfilepath,
        )


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

    D_columns: Tuple[List[int], List[int]]
    E_columns: Tuple[List[int], List[int]]
    UD_columns: List[int]
    UE_columns: List[int]

    def __repr__(self) -> str:
        return (
            f"PyIndices(\n"
            f"  current={self.current},\n"
            f"  forward={self.forward},\n"
            f"  purely_forward={self.purely_forward},\n"
            f"  backward={self.backward},\n"
            f"  both={self.both},\n"
            f"  non_backward={self.non_backward},\n"
            f"  static={self.static},\n"
            f"  dynamic={self.dynamic},\n"
            f"  dynamic_current={self.dynamic_current},\n"
            f"  current_in_dynamic={self.current_in_dynamic},\n"
            f"  forward_in_dynamic={self.forward_in_dynamic},\n"
            f"  backward_in_dynamic={self.backward_in_dynamic},\n"
            f"  current_in_dynamic_jacobian={self.current_in_dynamic_jacobian},\n"
            f"  current_in_static_jacobian={self.current_in_static_jacobian},\n"
            f"  exogenous={self.exogenous},\n"
            f"  n_endogenous={self.n_endogenous},\n"
            f"  D_columns={self.D_columns},\n"
            f"  E_columns={self.E_columns},\n"
            f"  UD_columns={self.UD_columns},\n"
            f"  UE_columns={self.UE_columns}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            current=list(julia_obj.current),
            forward=list(julia_obj.forward),
            purely_forward=list(julia_obj.purely_forward),
            backward=list(julia_obj.backward),
            both=list(julia_obj.both),
            non_backward=list(julia_obj.non_backward),
            static=list(julia_obj.static),
            dynamic=list(julia_obj.dynamic),
            dynamic_current=list(julia_obj.dynamic_current),
            current_in_dynamic=list(julia_obj.current_in_dynamic),
            forward_in_dynamic=list(julia_obj.forward_in_dynamic),
            backward_in_dynamic=list(julia_obj.backward_in_dynamic),
            current_in_dynamic_jacobian=list(julia_obj.current_in_dynamic_jacobian),
            current_in_static_jacobian=list(julia_obj.current_in_static_jacobian),
            exogenous=list(julia_obj.exogenous),
            n_endogenous=julia_obj.n_endogenous,
            D_columns=(list(julia_obj.D_columns.D), list(julia_obj.D_columns.jacobian)),
            E_columns=(list(julia_obj.E_columns.E), list(julia_obj.E_columns.jacobian)),
            UD_columns=list(julia_obj.UD_columns),
            UE_columns=list(julia_obj.UE_columns),
        )


@dataclass
class Model:
    endogenous_nbr: int
    exogenous_nbr: int
    lagged_exogenous_nbr: int
    exogenous_deterministic_nbr: int
    parameter_nbr: int
    original_endogenous_nbr: int
    lead_lag_incidence: np.ndarray
    n_static: int
    n_fwrd: int
    n_bkwrd: int
    n_both: int
    n_states: int
    DErows1: List[int]
    DErows2: List[int]
    n_dyn: int
    i_static: List[int]
    i_dyn: np.ndarray
    i_bkwrd: List[int]
    i_bkwrd_b: List[int]
    i_bkwrd_ns: List[int]
    i_fwrd: List[int]
    i_fwrd_b: List[int]
    i_fwrd_ns: List[int]
    i_both: List[int]
    i_non_states: List[int]
    p_static: List[int]
    p_bkwrd: List[int]
    p_bkwrd_b: List[int]
    p_fwrd: List[int]
    p_fwrd_b: List[int]
    p_both_b: List[int]
    p_both_f: List[int]
    i_current: List[int]
    p_current: List[int]
    n_current: int
    i_current_ns: List[int]
    p_current_ns: List[int]
    n_current_ns: int
    icolsD: List[int]
    jcolsD: List[int]
    icolsE: List[int]
    jcolsE: List[int]
    colsUD: List[int]
    colsUE: List[int]
    i_cur_fwrd: List[int]
    n_cur_fwrd: int
    p_cur_fwrd: List[int]
    i_cur_bkwrd: List[int]
    n_cur_bkwrd: int
    p_cur_bkwrd: List[int]
    i_cur_both: List[int]
    n_cur_both: int
    p_cur_both: List[int]
    gx_rows: List[int]
    hx_rows: List[int]
    i_current_exogenous: List[int]
    i_lagged_exogenous: List[int]
    serially_correlated_exogenous: List[int]
    Sigma_e: np.ndarray
    maximum_endo_lag: int
    maximum_endo_lead: int
    maximum_exo_lag: int
    maximum_exo_lead: int
    maximum_exo_det_lag: int
    maximum_exo_det_lead: int
    maximum_lag: int
    maximum_lead: int
    orig_maximum_endo_lag: int
    orig_maximum_endo_lead: int
    orig_maximum_exo_lag: int
    orig_maximum_exo_lead: int
    orig_maximum_exo_det_lag: int
    orig_maximum_exo_det_lead: int
    orig_maximum_lag: int
    orig_maximum_lead: int
    dynamic_indices: List[int]
    current_dynamic_indices: List[int]
    forward_indices_d: List[int]
    backward_indices_d: List[int]
    current_dynamic_indices_d: List[int]
    exogenous_indices: List[int]
    NNZDerivatives: List[int]
    auxiliary_variables: List[Dict[str, any]]
    mcps: List[Tuple[int, int, str, str]]
    dynamic_g1_sparse_rowval: List[int]
    dynamic_g1_sparse_colval: List[int]
    dynamic_g1_sparse_colptr: List[int]
    dynamic_g2_sparse_indices: List[List[int]]
    static_g1_sparse_rowval: List[int]
    static_g1_sparse_colptr: List[int]
    dynamic_tmp_nbr: List[int]
    static_tmp_nbr: List[int]
    ids: List[PyIndices]  # Assuming LRE.Indices is defined elsewhere

    def __repr__(self) -> str:
        return (
            f"Model(\n"
            f"  endogenous_nbr={self.endogenous_nbr},\n"
            f"  exogenous_nbr={self.exogenous_nbr},\n"
            f"  lagged_exogenous_nbr={self.lagged_exogenous_nbr},\n"
            f"  exogenous_deterministic_nbr={self.exogenous_deterministic_nbr},\n"
            f"  parameter_nbr={self.parameter_nbr},\n"
            f"  original_endogenous_nbr={self.original_endogenous_nbr},\n"
            f"  lead_lag_incidence={self.lead_lag_incidence},\n"
            f"  n_static={self.n_static},\n"
            f"  n_fwrd={self.n_fwrd},\n"
            f"  n_bkwrd={self.n_bkwrd},\n"
            f"  n_both={self.n_both},\n"
            f"  n_states={self.n_states},\n"
            f"  DErows1={self.DErows1},\n"
            f"  DErows2={self.DErows2},\n"
            f"  n_dyn={self.n_dyn},\n"
            f"  i_static={self.i_static},\n"
            f"  i_dyn={self.i_dyn},\n"
            f"  i_bkwrd={self.i_bkwrd},\n"
            f"  i_bkwrd_b={self.i_bkwrd_b},\n"
            f"  i_bkwrd_ns={self.i_bkwrd_ns},\n"
            f"  i_fwrd={self.i_fwrd},\n"
            f"  i_fwrd_b={self.i_fwrd_b},\n"
            f"  i_fwrd_ns={self.i_fwrd_ns},\n"
            f"  i_both={self.i_both},\n"
            f"  i_non_states={self.i_non_states},\n"
            f"  p_static={self.p_static},\n"
            f"  p_bkwrd={self.p_bkwrd},\n"
            f"  p_bkwrd_b={self.p_bkwrd_b},\n"
            f"  p_fwrd={self.p_fwrd},\n"
            f"  p_fwrd_b={self.p_fwrd_b},\n"
            f"  p_both_b={self.p_both_b},\n"
            f"  p_both_f={self.p_both_f},\n"
            f"  i_current={self.i_current},\n"
            f"  p_current={self.p_current},\n"
            f"  n_current={self.n_current},\n"
            f"  i_current_ns={self.i_current_ns},\n"
            f"  p_current_ns={self.p_current_ns},\n"
            f"  n_current_ns={self.n_current_ns},\n"
            f"  icolsD={self.icolsD},\n"
            f"  jcolsD={self.jcolsD},\n"
            f"  icolsE={self.icolsE},\n"
            f"  jcolsE={self.jcolsE},\n"
            f"  colsUD={self.colsUD},\n"
            f"  colsUE={self.colsUE},\n"
            f"  i_cur_fwrd={self.i_cur_fwrd},\n"
            f"  n_cur_fwrd={self.n_cur_fwrd},\n"
            f"  p_cur_fwrd={self.p_cur_fwrd},\n"
            f"  i_cur_bkwrd={self.i_cur_bkwrd},\n"
            f"  n_cur_bkwrd={self.n_cur_bkwrd},\n"
            f"  p_cur_bkwrd={self.p_cur_bkwrd},\n"
            f"  i_cur_both={self.i_cur_both},\n"
            f"  n_cur_both={self.n_cur_both},\n"
            f"  p_cur_both={self.p_cur_both},\n"
            f"  gx_rows={self.gx_rows},\n"
            f"  hx_rows={self.hx_rows},\n"
            f"  i_current_exogenous={self.i_current_exogenous},\n"
            f"  i_lagged_exogenous={self.i_lagged_exogenous},\n"
            f"  serially_correlated_exogenous={self.serially_correlated_exogenous},\n"
            f"  Sigma_e={self.Sigma_e},\n"
            f"  maximum_endo_lag={self.maximum_endo_lag},\n"
            f"  maximum_endo_lead={self.maximum_endo_lead},\n"
            f"  maximum_exo_lag={self.maximum_exo_lag},\n"
            f"  maximum_exo_lead={self.maximum_exo_lead},\n"
            f"  maximum_exo_det_lag={self.maximum_exo_det_lag},\n"
            f"  maximum_exo_det_lead={self.maximum_exo_det_lead},\n"
            f"  maximum_lag={self.maximum_lag},\n"
            f"  maximum_lead={self.maximum_lead},\n"
            f"  orig_maximum_endo_lag={self.orig_maximum_endo_lag},\n"
            f"  orig_maximum_endo_lead={self.orig_maximum_endo_lead},\n"
            f"  orig_maximum_exo_lag={self.orig_maximum_exo_lag},\n"
            f"  orig_maximum_exo_lead={self.orig_maximum_exo_lead},\n"
            f"  orig_maximum_exo_det_lag={self.orig_maximum_exo_det_lag},\n"
            f"  orig_maximum_exo_det_lead={self.orig_maximum_exo_det_lead},\n"
            f"  orig_maximum_lag={self.orig_maximum_lag},\n"
            f"  orig_maximum_lead={self.orig_maximum_lead},\n"
            f"  dynamic_indices={self.dynamic_indices},\n"
            f"  current_dynamic_indices={self.current_dynamic_indices},\n"
            f"  forward_indices_d={self.forward_indices_d},\n"
            f"  backward_indices_d={self.backward_indices_d},\n"
            f"  current_dynamic_indices_d={self.current_dynamic_indices_d},\n"
            f"  exogenous_indices={self.exogenous_indices},\n"
            f"  NNZDerivatives={self.NNZDerivatives},\n"
            f"  auxiliary_variables={self.auxiliary_variables},\n"
            f"  mcps={self.mcps},\n"
            f"  dynamic_g1_sparse_rowval={self.dynamic_g1_sparse_rowval},\n"
            f"  dynamic_g1_sparse_colval={self.dynamic_g1_sparse_colval},\n"
            f"  dynamic_g1_sparse_colptr={self.dynamic_g1_sparse_colptr},\n"
            f"  dynamic_g2_sparse_indices={self.dynamic_g2_sparse_indices},\n"
            f"  static_g1_sparse_rowval={self.static_g1_sparse_rowval},\n"
            f"  static_g1_sparse_colptr={self.static_g1_sparse_colptr},\n"
            f"  dynamic_tmp_nbr={self.dynamic_tmp_nbr},\n"
            f"  static_tmp_nbr={self.static_tmp_nbr},\n"
            f"  ids={self.ids}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_model) -> Self:
        return Model(
            endogenous_nbr=get_member(jl_model, "endogenous_nbr"),
            exogenous_nbr=get_member(jl_model, "exogenous_nbr"),
            lagged_exogenous_nbr=get_member(jl_model, "lagged_exogenous_nbr"),
            exogenous_deterministic_nbr=get_member(
                jl_model, "exogenous_deterministic_nbr"
            ),
            parameter_nbr=get_member(jl_model, "parameter_nbr"),
            original_endogenous_nbr=get_member(jl_model, "original_endogenous_nbr"),
            lead_lag_incidence=get_member(jl_model, "lead_lag_incidence").to_numpy()
            if get_member(jl_model, "lead_lag_incidence")
            else None,
            n_static=get_member(jl_model, "n_static"),
            n_fwrd=get_member(jl_model, "n_fwrd"),
            n_bkwrd=get_member(jl_model, "n_bkwrd"),
            n_both=get_member(jl_model, "n_both"),
            n_states=get_member(jl_model, "n_states"),
            DErows1=list(get_member(jl_model, "DErows1", [])),
            DErows2=list(get_member(jl_model, "DErows2", [])),
            n_dyn=get_member(jl_model, "n_dyn"),
            i_static=list(get_member(jl_model, "i_static", [])),
            i_dyn=get_member(jl_model, "i_dyn").to_numpy()
            if get_member(jl_model, "i_dyn")
            else None,
            i_bkwrd=list(get_member(jl_model, "i_bkwrd", [])),
            i_bkwrd_b=list(get_member(jl_model, "i_bkwrd_b", [])),
            i_bkwrd_ns=list(get_member(jl_model, "i_bkwrd_ns", [])),
            i_fwrd=list(get_member(jl_model, "i_fwrd", [])),
            i_fwrd_b=list(get_member(jl_model, "i_fwrd_b", [])),
            i_fwrd_ns=list(get_member(jl_model, "i_fwrd_ns", [])),
            i_both=list(get_member(jl_model, "i_both", [])),
            i_non_states=list(get_member(jl_model, "i_non_states", [])),
            p_static=list(get_member(jl_model, "p_static", [])),
            p_bkwrd=list(get_member(jl_model, "p_bkwrd", [])),
            p_bkwrd_b=list(get_member(jl_model, "p_bkwrd_b", [])),
            p_fwrd=list(get_member(jl_model, "p_fwrd", [])),
            p_fwrd_b=list(get_member(jl_model, "p_fwrd_b", [])),
            p_both_b=list(get_member(jl_model, "p_both_b", [])),
            p_both_f=list(get_member(jl_model, "p_both_f", [])),
            i_current=list(get_member(jl_model, "i_current", [])),
            p_current=list(get_member(jl_model, "p_current", [])),
            n_current=get_member(jl_model, "n_current"),
            i_current_ns=list(get_member(jl_model, "i_current_ns", [])),
            p_current_ns=list(get_member(jl_model, "p_current_ns", [])),
            n_current_ns=get_member(jl_model, "n_current_ns"),
            icolsD=list(get_member(jl_model, "icolsD", [])),
            jcolsD=list(get_member(jl_model, "jcolsD", [])),
            icolsE=list(get_member(jl_model, "icolsE", [])),
            jcolsE=list(get_member(jl_model, "jcolsE", [])),
            colsUD=list(get_member(jl_model, "colsUD", [])),
            colsUE=list(get_member(jl_model, "colsUE", [])),
            i_cur_fwrd=list(get_member(jl_model, "i_cur_fwrd", [])),
            n_cur_fwrd=get_member(jl_model, "n_cur_fwrd"),
            p_cur_fwrd=list(get_member(jl_model, "p_cur_fwrd", [])),
            i_cur_bkwrd=list(get_member(jl_model, "i_cur_bkwrd", [])),
            n_cur_bkwrd=get_member(jl_model, "n_cur_bkwrd"),
            p_cur_bkwrd=list(get_member(jl_model, "p_cur_bkwrd", [])),
            i_cur_both=list(get_member(jl_model, "i_cur_both", [])),
            n_cur_both=get_member(jl_model, "n_cur_both"),
            p_cur_both=list(get_member(jl_model, "p_cur_both", [])),
            gx_rows=list(get_member(jl_model, "gx_rows", [])),
            hx_rows=list(get_member(jl_model, "hx_rows", [])),
            i_current_exogenous=list(get_member(jl_model, "i_current_exogenous", [])),
            i_lagged_exogenous=list(get_member(jl_model, "i_lagged_exogenous", [])),
            serially_correlated_exogenous=list(
                get_member(jl_model, "serially_correlated_exogenous", [])
            ),
            Sigma_e=get_member(jl_model, "Sigma_e").to_numpy()
            if get_member(jl_model, "Sigma_e")
            else None,
            maximum_endo_lag=get_member(jl_model, "maximum_endo_lag"),
            maximum_endo_lead=get_member(jl_model, "maximum_endo_lead"),
            maximum_exo_lag=get_member(jl_model, "maximum_exo_lag"),
            maximum_exo_lead=get_member(jl_model, "maximum_exo_lead"),
            maximum_exo_det_lag=get_member(jl_model, "maximum_exo_det_lag"),
            maximum_exo_det_lead=get_member(jl_model, "maximum_exo_det_lead"),
            maximum_lag=get_member(jl_model, "maximum_lag"),
            maximum_lead=get_member(jl_model, "maximum_lead"),
            orig_maximum_endo_lag=get_member(jl_model, "orig_maximum_endo_lag"),
            orig_maximum_endo_lead=get_member(jl_model, "orig_maximum_endo_lead"),
            orig_maximum_exo_lag=get_member(jl_model, "orig_maximum_exo_lag"),
            orig_maximum_exo_lead=get_member(jl_model, "orig_maximum_exo_lead"),
            orig_maximum_exo_det_lag=get_member(jl_model, "orig_maximum_exo_det_lag"),
            orig_maximum_exo_det_lead=get_member(jl_model, "orig_maximum_exo_det_lead"),
            orig_maximum_lag=get_member(jl_model, "orig_maximum_lag"),
            orig_maximum_lead=get_member(jl_model, "orig_maximum_lead"),
            dynamic_indices=list(get_member(jl_model, "dynamic_indices", [])),
            current_dynamic_indices=list(
                get_member(jl_model, "current_dynamic_indices", [])
            ),
            forward_indices_d=list(get_member(jl_model, "forward_indices_d", [])),
            backward_indices_d=list(get_member(jl_model, "backward_indices_d", [])),
            current_dynamic_indices_d=list(
                get_member(jl_model, "current_dynamic_indices_d", [])
            ),
            exogenous_indices=list(get_member(jl_model, "exogenous_indices", [])),
            NNZDerivatives=list(get_member(jl_model, "NNZDerivatives", [])),
            auxiliary_variables=list(get_member(jl_model, "auxiliary_variables", [])),
            mcps=list(get_member(jl_model, "mcps", [])),
            dynamic_g1_sparse_rowval=list(
                get_member(jl_model, "dynamic_g1_sparse_rowval", [])
            ),
            dynamic_g1_sparse_colval=list(
                get_member(jl_model, "dynamic_g1_sparse_colval", [])
            ),
            dynamic_g1_sparse_colptr=list(
                get_member(jl_model, "dynamic_g1_sparse_colptr", [])
            ),
            dynamic_g2_sparse_indices=[
                list(indices)
                for indices in get_member(jl_model, "dynamic_g2_sparse_indices", [])
            ],
            static_g1_sparse_rowval=list(
                get_member(jl_model, "static_g1_sparse_rowval", [])
            ),
            static_g1_sparse_colptr=list(
                get_member(jl_model, "static_g1_sparse_colptr", [])
            ),
            dynamic_tmp_nbr=list(get_member(jl_model, "dynamic_tmp_nbr", [])),
            static_tmp_nbr=list(get_member(jl_model, "static_tmp_nbr", [])),
            ids=PyIndices.from_julia(get_member(jl_model, "ids", [])),
        )


@dataclass
class Simulation:
    firstperiod: int  # Replace Any with the appropriate type for PeriodsSinceEpoch
    lastperiod: int  # Replace Any with the appropriate type for PeriodsSinceEpoch
    name: str
    statement: str
    data: pd.DataFrame  # Assuming AxisArrayTable can be represented as a DataFrame

    def __repr__(self) -> str:
        return (
            f"Simulation(\n"
            f"  firstperiod={self.firstperiod},\n"
            f"  lastperiod={self.lastperiod},\n"
            f"  name={self.name},\n"
            f"  statement={self.statement},\n"
            f"  data={self.data}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_simulation) -> Self:
        return Simulation(
            firstperiod=jl_simulation.firstperiod,
            lastperiod=jl_simulation.lastperiod,
            name=jl_simulation.name,
            statement=jl_simulation.statement,
            data=jl_simulation.data,
        )


@dataclass
class Trends:
    endogenous_steady_state: List[float] = field(default_factory=list)
    endogenous_terminal_steady_state: List[float] = field(default_factory=list)
    endogenous_linear_trend: List[float] = field(default_factory=list)
    endogenous_quadratic_trend: List[float] = field(default_factory=list)
    exogenous_steady_state: List[float] = field(default_factory=list)
    exogenous_terminal_steady_state: List[float] = field(default_factory=list)
    exogenous_linear_trend: List[float] = field(default_factory=list)
    exogenous_quadratic_trend: List[float] = field(default_factory=list)
    exogenous_det_steady_state: List[float] = field(default_factory=list)
    exogenous_det_terminal_steady_state: List[float] = field(default_factory=list)
    exogenous_det_linear_trend: List[float] = field(default_factory=list)
    exogenous_det_quadratic_trend: List[float] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"Trends(\n"
            f"  endogenous_steady_state={self.endogenous_steady_state},\n"
            f"  endogenous_terminal_steady_state={self.endogenous_terminal_steady_state},\n"
            f"  endogenous_linear_trend={self.endogenous_linear_trend},\n"
            f"  endogenous_quadratic_trend={self.endogenous_quadratic_trend},\n"
            f"  exogenous_steady_state={self.exogenous_steady_state},\n"
            f"  exogenous_terminal_steady_state={self.exogenous_terminal_steady_state},\n"
            f"  exogenous_linear_trend={self.exogenous_linear_trend},\n"
            f"  exogenous_quadratic_trend={self.exogenous_quadratic_trend},\n"
            f"  exogenous_det_steady_state={self.exogenous_det_steady_state},\n"
            f"  exogenous_det_terminal_steady_state={self.exogenous_det_terminal_steady_state},\n"
            f"  exogenous_det_linear_trend={self.exogenous_det_linear_trend},\n"
            f"  exogenous_det_quadratic_trend={self.exogenous_det_quadratic_trend}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_trends) -> Self:
        return Trends(
            endogenous_steady_state=list(jl_trends.endogenous_steady_state),
            endogenous_terminal_steady_state=list(
                jl_trends.endogenous_terminal_steady_state
            ),
            endogenous_linear_trend=list(jl_trends.endogenous_linear_trend),
            endogenous_quadratic_trend=list(jl_trends.endogenous_quadratic_trend),
            exogenous_steady_state=list(jl_trends.exogenous_steady_state),
            exogenous_terminal_steady_state=list(
                jl_trends.exogenous_terminal_steady_state
            ),
            exogenous_linear_trend=list(jl_trends.exogenous_linear_trend),
            exogenous_quadratic_trend=list(jl_trends.exogenous_quadratic_trend),
            exogenous_det_steady_state=list(jl_trends.exogenous_det_steady_state),
            exogenous_det_terminal_steady_state=list(
                jl_trends.exogenous_det_terminal_steady_state
            ),
            exogenous_det_linear_trend=list(jl_trends.exogenous_det_linear_trend),
            exogenous_det_quadratic_trend=list(jl_trends.exogenous_det_quadratic_trend),
        )


@dataclass
class EstimationResults:
    posterior_mode: List[Any] = field(default_factory=list)
    transformed_posterior_mode: List[Any] = field(default_factory=list)
    posterior_mode_std: List[Any] = field(default_factory=list)
    transformed_posterior_mode_std: List[Any] = field(default_factory=list)
    posterior_mode_covariance: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0))
    )
    transformed_posterior_mode_covariance: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0))
    )
    posterior_mcmc_chains_nbr: int = 0

    def __repr__(self) -> str:
        return (
            f"EstimationResults(\n"
            f"  posterior_mode={self.posterior_mode},\n"
            f"  transformed_posterior_mode={self.transformed_posterior_mode},\n"
            f"  posterior_mode_std={self.posterior_mode_std},\n"
            f"  transformed_posterior_mode_std={self.transformed_posterior_mode_std},\n"
            f"  posterior_mode_covariance={self.posterior_mode_covariance},\n"
            f"  transformed_posterior_mode_covariance={self.transformed_posterior_mode_covariance},\n"
            f"  posterior_mcmc_chains_nbr={self.posterior_mcmc_chains_nbr}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_estimationresults) -> Self:
        return EstimationResults(
            posterior_mode=list(jl_estimationresults.posterior_mode),
            transformed_posterior_mode=list(
                jl_estimationresults.transformed_posterior_mode
            ),
            posterior_mode_std=list(jl_estimationresults.posterior_mode_std),
            transformed_posterior_mode_std=list(
                jl_estimationresults.transformed_posterior_mode_std
            ),
            posterior_mode_covariance=jl_estimationresults.posterior_mode_covariance.to_numpy(),
            transformed_posterior_mode_covariance=jl_estimationresults.transformed_posterior_mode_covariance.to_numpy(),
            posterior_mcmc_chains_nbr=jl_estimationresults.posterior_mcmc_chains_nbr,
        )


@dataclass
class LinearRationalExpectationsResults:
    eigenvalues: np.ndarray = field(
        default_factory=lambda: np.array([], dtype=np.complex128)
    )
    g1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    gs1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    hs1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    gns1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    hns1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    g1_1: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    g1_2: np.ndarray = field(default_factory=lambda: np.zeros((0, 0), dtype=np.float64))
    endogenous_variance: np.ndarray = field(
        default_factory=lambda: np.zeros((0, 0), dtype=np.float64)
    )
    stationary_variables: np.ndarray = field(
        default_factory=lambda: np.zeros(0, dtype=bool)
    )

    def __repr__(self) -> str:
        return (
            f"LinearRationalExpectationsResults(\n"
            f"  eigenvalues={self.eigenvalues},\n"
            f"  g1={self.g1},\n"
            f"  gs1={self.gs1},\n"
            f"  hs1={self.hs1},\n"
            f"  gns1={self.gns1},\n"
            f"  hns1={self.hns1},\n"
            f"  g1_1={self.g1_1},\n"
            f"  g1_2={self.g1_2},\n"
            f"  endogenous_variance={self.endogenous_variance},\n"
            f"  stationary_variables={self.stationary_variables}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_linearrationalexpectationsresults) -> Self:
        return LinearRationalExpectationsResults(
            eigenvalues=jl_linearrationalexpectationsresults.eigenvalues.to_numpy(),
            g1=jl_linearrationalexpectationsresults.g1.to_numpy(),
            gs1=jl_linearrationalexpectationsresults.gs1.to_numpy(),
            hs1=jl_linearrationalexpectationsresults.hs1.to_numpy(),
            gns1=jl_linearrationalexpectationsresults.gns1.to_numpy(),
            hns1=jl_linearrationalexpectationsresults.hns1.to_numpy(),
            g1_1=jl_linearrationalexpectationsresults.g1_1.to_numpy(),
            g1_2=jl_linearrationalexpectationsresults.g1_2.to_numpy(),
            endogenous_variance=jl_linearrationalexpectationsresults.endogenous_variance.to_numpy(),
            stationary_variables=jl_linearrationalexpectationsresults.stationary_variables.to_numpy(),
        )


class PySGSolver(Enum):
    NLsolver = 1
    NonlinearSolver = 2
    PATHSolver = 3

    @classmethod
    def from_julia(cls, jl_sgsolver) -> Self:
        return PySGSolver(
            int(
                str(repr(jl_sgsolver))
                .replace("Julia: NLsolver::SGSolver = ", "")
                .replace("Julia: NonlinearSolver::SGSolver = ", "")
                .replace("Julia: PATHSolver::SGSolver = ", "")
            )
        )


libtas_path = os.getenv("LIBTASMANIAN_PATH")
if libtas_path:
    TASlib = ctypes.CDLL(libtas_path)  # Load the shared library
else:
    TASlib = None


@dataclass
class PyTasmanianSG:
    pGrid: type[
        ctypes._Pointer
    ]  # ctypes.POINTER(ctypes.c_void_p) Corresponds to Ptr{Nothing} in Julia
    dimensions: int
    outputs: int
    depth: int

    def __repr__(self) -> str:
        return (
            f"PyTasmanianSG(\n"
            f"  pGrid={self.pGrid},\n"
            f"  dimensions={self.dimensions},\n"
            f"  outputs={self.outputs},\n"
            f"  depth={self.depth}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_tasmaniansg) -> Self:
        if not TASlib:
            raise ValueError("It looks like Tasmanian is not installed. Please install from https://github.com/ORNL/TASMANIAN and set LIBTASMANIAN_PATH")
        c_func = getattr(TASlib, "tsgConstructTasmanianSparseGrid")
        c_func.restype = ctypes.POINTER(ctypes.c_void_p)
        pGrid = c_func()

        if not pGrid:
            raise MemoryError("Out of memory")

        return cls(
            pGrid=pGrid,
            dimensions=jl_tasmaniansg.dimensions,
            outputs=jl_tasmaniansg.outputs,
            depth=jl_tasmaniansg.depth,
        )


T = TypeVar("T")  # Placeholder for concrete_jac
N = TypeVar("N")  # Placeholder for name


@dataclass
class PyGeneralizedFirstOrderAlgorithm(Generic[T, N]):
    linesearch: Any
    trustregion: Any
    descent: Any
    max_shrink_times: int
    jacobian_ad: Any
    forward_ad: Any
    reverse_ad: Any

    def __repr__(self) -> str:
        return (
            f"PyGeneralizedFirstOrderAlgorithm(\n"
            f"  linesearch={self.linesearch},\n"
            f"  trustregion={self.trustregion},\n"
            f"  descent={self.descent},\n"
            f"  max_shrink_times={self.max_shrink_times},\n"
            f"  jacobian_ad={self.jacobian_ad},\n"
            f"  forward_ad={self.forward_ad},\n"
            f"  reverse_ad={self.reverse_ad}\n"
            f")"
        )

    @classmethod
    def from_julia(
        cls,
        jl_generalizedfirstorderalgorithm,
    ):
        return cls(
            linesearch=jl_generalizedfirstorderalgorithm.linesearch,
            trustregion=jl_generalizedfirstorderalgorithm.trustregion,
            descent=jl_generalizedfirstorderalgorithm.descent,
            max_shrink_times=jl_generalizedfirstorderalgorithm.max_shrink_times,
            jacobian_ad=jl_generalizedfirstorderalgorithm.jacobian_ad,
            forward_ad=jl_generalizedfirstorderalgorithm.forward_ad,
            reverse_ad=jl_generalizedfirstorderalgorithm.reverse_ad,
        )


@dataclass
class PySparsegridsResults:
    average_error: float
    average_iteration_time: float
    drawsnbr: int
    equation_average_errors: List[float]
    equation_quantile_errors: List[float]
    ftol: float
    grid: PyTasmanianSG
    gridDepth: int
    gridOrder: int
    gridRule: str
    iterRefStart: int
    maxRef: int
    mcp: bool
    method: PyGeneralizedFirstOrderAlgorithm
    quantile_error: float
    quantile_probability: float
    solver: PySGSolver
    surplThreshold: float

    def __repr__(self) -> str:
        return (
            f"PySparsegridsResults(\n"
            f"  average_error={self.average_error},\n"
            f"  average_iteration_time={self.average_iteration_time},\n"
            f"  drawsnbr={self.drawsnbr},\n"
            f"  equation_average_errors={self.equation_average_errors},\n"
            f"  equation_quantile_errors={self.equation_quantile_errors},\n"
            f"  ftol={self.ftol},\n"
            f"  grid={self.grid},\n"
            f"  gridDepth={self.gridDepth},\n"
            f"  gridOrder={self.gridOrder},\n"
            f"  gridRule={self.gridRule},\n"
            f"  iterRefStart={self.iterRefStart},\n"
            f"  maxRef={self.maxRef},\n"
            f"  mcp={self.mcp},\n"
            f"  method={self.method},\n"
            f"  quantile_error={self.quantile_error},\n"
            f"  quantile_probability={self.quantile_probability},\n"
            f"  solver={self.solver},\n"
            f"  surplThreshold={self.surplThreshold}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, julia_obj):
        return cls(
            average_error=julia_obj.average_error,
            average_iteration_time=julia_obj.average_iteration_time,
            drawsnbr=julia_obj.drawsnbr,
            equation_average_errors=list(julia_obj.equation_average_errors),
            equation_quantile_errors=list(julia_obj.equation_quantile_errors),
            ftol=julia_obj.ftol,
            grid=julia_obj.grid,  # Assuming grid can be directly mapped, or further conversion may be needed
            gridDepth=julia_obj.gridDepth,
            gridOrder=julia_obj.gridOrder,
            gridRule=julia_obj.gridRule,
            iterRefStart=julia_obj.iterRefStart,
            maxRef=julia_obj.maxRef,
            mcp=julia_obj.mcp,
            method=julia_obj.method,  # Assuming method can be directly mapped, or further conversion may be needed
            quantile_error=julia_obj.quantile_error,
            quantile_probability=julia_obj.quantile_probability,
            solver=julia_obj.solver,  # Assuming solver can be directly mapped, or further conversion may be needed
            surplThreshold=julia_obj.surplThreshold,
        )


@dataclass
class ModelResults:
    irfs: Dict[
        str, pd.DataFrame
    ]  # Assuming AxisArrayTable can be represented as a DataFrame
    trends: Trends
    stationary_variables: List[bool]
    estimation: EstimationResults
    filter: pd.DataFrame  # Assuming AxisArrayTable can be represented as a DataFrame
    forecast: List[
        pd.DataFrame
    ]  # Assuming AxisArrayTable can be represented as a DataFrame
    initial_smoother: pd.DataFrame  # Assuming AxisArrayTable can be represented as a DataFrame
    linearrationalexpectations: LinearRationalExpectationsResults
    simulations: List[Simulation]
    smoother: pd.DataFrame  # Assuming AxisArrayTable can be represented as a DataFrame
    solution_derivatives: List[
        np.ndarray
    ]  # Assuming Matrix{Float64} can be represented as a numpy array
    sparesegrids: PySparsegridsResults

    def __repr__(self) -> str:
        return (
            f"ModelResults(\n"
            f"  irfs={self.irfs},\n"
            f"  trends={self.trends},\n"
            f"  stationary_variables={self.stationary_variables},\n"
            f"  estimation={self.estimation},\n"
            f"  filter={self.filter},\n"
            f"  forecast={self.forecast},\n"
            f"  initial_smoother={self.initial_smoother},\n"
            f"  linearrationalexpectations={self.linearrationalexpectations},\n"
            f"  simulations={self.simulations},\n"
            f"  smoother={self.smoother},\n"
            f"  solution_derivatives={self.solution_derivatives},\n"
            f"  sparesegrids={self.sparesegrids}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_modelresults) -> Self:
        return ModelResults(
            irfs={
                repr(k).replace("Julia: ", ""): v
                for k, v in jl_modelresults.irfs.items()
            },
            trends=Trends.from_julia(jl_modelresults.trends),
            stationary_variables=list(jl_modelresults.stationary_variables),
            estimation=EstimationResults.from_julia(jl_modelresults.estimation),
            filter=jl_modelresults.filter,
            forecast=list(jl_modelresults.forecast),
            initial_smoother=jl_modelresults.initial_smoother,
            linearrationalexpectations=LinearRationalExpectationsResults.from_julia(
                jl_modelresults.linearrationalexpectations
            ),
            simulations=[Simulation.from_julia(s) for s in jl_modelresults.simulations],
            smoother=jl_modelresults.smoother,
            solution_derivatives=[
                sd.to_numpy() for sd in jl_modelresults.solution_derivatives
            ],
            sparesegrids=None,
            # (
            #     PySparsegridsResults.from_julia(jl_modelresults.sparesegrids)
            #     if jl_modelresults.sparesegrids
            #     else None
            # ),
        )


@dataclass
class Results:
    model_results: List[ModelResults]

    def __repr__(self) -> str:
        return f"Results(\n" f" model_results={self.model_results}\n" ")"

    @classmethod
    def from_julia(cls, jl_results) -> Self:
        return Results(
            model_results=[
                ModelResults.from_julia(jlmr) for jlmr in jl_results.model_results
            ]
        )


def distribution_from_julia(
    jl_distribution,
) -> Union[
    stats.rv_continuous, stats.rv_discrete, stats._multivariate.multi_rv_generic, None
]:
    conversion_map = {
        "Normal": lambda dist: stats.norm(loc=dist.μ, scale=dist.σ),
        "Exponential": lambda dist: stats.expon(scale=1 / dist.θ),
        "Uniform": lambda dist: stats.uniform(loc=dist.a, scale=dist.b - dist.a),
        "Gamma": lambda dist: stats.gamma(a=dist.α, scale=1 / dist.θ),
        "Beta": lambda dist: stats.beta(a=dist.α, b=dist.β),
        "Binomial": lambda dist: stats.binom(n=dist.n, p=dist.p),
        "Poisson": lambda dist: stats.poisson(mu=dist.λ),
        "Geometric": lambda dist: stats.geom(p=dist.p),
        "NegativeBinomial": lambda dist: stats.nbinom(n=dist.r, p=dist.p),
        "ChiSquared": lambda dist: stats.chi2(df=dist.ν),
        "TDist": lambda dist: stats.t(df=dist.ν),
        "Laplace": lambda dist: stats.laplace(loc=dist.μ, scale=dist.β),
        "Cauchy": lambda dist: stats.cauchy(loc=dist.x0, scale=dist.γ),
        "LogNormal": lambda dist: stats.lognorm(s=dist.σ, scale=np.exp(dist.μ)),
        "Weibull": lambda dist: stats.weibull_min(c=dist.k, scale=dist.λ),
        "Gumbel": lambda dist: stats.gumbel_r(loc=dist.μ, scale=dist.β),
        "MvNormal": lambda dist: stats.multivariate_normal(
            mean=np.array(dist.μ), cov=np.array(dist.Σ)
        ),
        "MvTDist": lambda dist: stats.multivariate_t(
            loc=np.array(dist.μ), shape=np.array(dist.Σ), df=dist.ν
        ),
        "Dirichlet": lambda dist: stats.dirichlet(alpha=np.array(dist.α)),
        "Bernoulli": lambda dist: stats.bernoulli(p=dist.p),
        "Categorical": lambda dist: stats.multinomial(n=1, p=np.array(dist.p)),
        "Multinomial": lambda dist: stats.multinomial(n=dist.n, p=np.array(dist.p)),
    }

    # Get the Julia distribution type name
    julia_dist_type = str(type(jl_distribution)).split(".")[-1].strip("'>")

    # Convert the Julia distribution to a scipy.stats distribution
    if julia_dist_type in conversion_map:
        return conversion_map[julia_dist_type](jl_distribution)
    else:
        raise ValueError(
            f"No conversion available for Julia distribution type: {julia_dist_type}"
        )


@dataclass
class EstimatedParameters:
    index: List[Union[int, Tuple[int, int]]] = field(default_factory=list)
    initialvalue: List[Union[float, None]] = field(
        default_factory=list
    )  # Using None for Missing
    ml_maximizer: List[float] = field(default_factory=list)
    name: List[Union[str, Tuple[str, str]]] = field(default_factory=list)
    parametertype: List[EstimatedParameterType] = field(default_factory=list)
    posterior_mean: List[float] = field(default_factory=list)
    posterior_median: List[float] = field(default_factory=list)
    posterior_mode: List[float] = field(default_factory=list)
    posterior_sd: List[float] = field(default_factory=list)
    posterior_hpdi_lb: List[float] = field(default_factory=list)
    posterior_hpdi_ub: List[float] = field(default_factory=list)
    prior: List[
        Union[
            stats.rv_continuous, stats.rv_discrete, stats._multivariate.multi_rv_generic
        ]
    ] = field(default_factory=list)

    def __len__(self):
        return len(self.prior)

    def __repr__(self) -> str:
        return (
            f"EstimatedParameters(\n"
            f"  index={self.index},\n"
            f"  initialvalue={self.initialvalue},\n"
            f"  ml_maximizer={self.ml_maximizer},\n"
            f"  name={self.name},\n"
            f"  parametertype={self.parametertype},\n"
            f"  posterior_mean={self.posterior_mean},\n"
            f"  posterior_median={self.posterior_median},\n"
            f"  posterior_mode={self.posterior_mode},\n"
            f"  posterior_sd={self.posterior_sd},\n"
            f"  posterior_hpdi_lb={self.posterior_hpdi_lb},\n"
            f"  posterior_hpdi_ub={self.posterior_hpdi_ub},\n"
            f"  prior={self.prior}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_estimatedparameters) -> Self:
        return EstimatedParameters(
            index=list(jl_estimatedparameters.index),
            initialvalue=list(jl_estimatedparameters.initialvalue),
            ml_maximizer=list(jl_estimatedparameters.ml_maximizer),
            name=list(jl_estimatedparameters.name),
            parametertype=[
                EstimatedParameterType.from_julia(ept)
                for ept in jl_estimatedparameters.parametertype
            ],
            posterior_mean=list(jl_estimatedparameters.posterior_mean),
            posterior_median=list(jl_estimatedparameters.posterior_median),
            posterior_mode=list(jl_estimatedparameters.posterior_mode),
            posterior_sd=list(jl_estimatedparameters.posterior_sd),
            posterior_hpdi_lb=list(jl_estimatedparameters.posterior_hpdi_lb),
            posterior_hpdi_ub=list(jl_estimatedparameters.posterior_hpdi_ub),
            prior=[distribution_from_julia(p) for p in jl_estimatedparameters.prior],
        )


@dataclass
class Work:
    analytical_steadystate_variables: List[int] = field(default_factory=list)
    data: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    datafile: str = ""
    params: List[float] = field(default_factory=list)
    residuals: List[float] = field(default_factory=list)
    dynamic_variables: List[float] = field(default_factory=list)
    exogenous_variables: List[float] = field(default_factory=list)
    observed_variables: List[str] = field(default_factory=list)
    Sigma_m: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    jacobian: np.ndarray = field(default_factory=lambda: np.empty((0, 0)))
    qr_jacobian: np.ndarray = field(default_factory=lambda: np.empty((0, 0)))
    model_has_trend: List[bool] = field(default_factory=lambda: [False])
    histval: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=object))
    homotopy_setup: List[
        Tuple[str, "SymbolType", int, float, Union[float, None]]
    ] = field(default_factory=list)
    initval_endogenous: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    initval_exogenous: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    initval_exogenous_deterministic: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    endval_endogenous: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    endval_exogenous: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    endval_exogenous_deterministic: np.ndarray = field(
        default_factory=lambda: np.empty((0, 0), dtype=object)
    )
    scenario: Dict[Any, Dict[str, Dict[Any, Tuple[float, str]]]] = field(
        default_factory=dict
    )
    shocks: List[float] = field(default_factory=list)
    perfect_foresight_setup: Dict[str, Any] = field(
        default_factory=lambda: {"periods": 0, "datafile": ""}
    )
    estimated_parameters: EstimatedParameters = field(
        default_factory=lambda: EstimatedParameters()
    )

    def __repr__(self) -> str:
        return (
            f"Work(\n"
            f"  analytical_steadystate_variables={self.analytical_steadystate_variables},\n"
            f"  data={self.data},\n"
            f"  datafile={self.datafile},\n"
            f"  params={self.params},\n"
            f"  residuals={self.residuals},\n"
            f"  dynamic_variables={self.dynamic_variables},\n"
            f"  exogenous_variables={self.exogenous_variables},\n"
            f"  observed_variables={self.observed_variables},\n"
            f"  Sigma_m={self.Sigma_m},\n"
            f"  jacobian={self.jacobian},\n"
            f"  qr_jacobian={self.qr_jacobian},\n"
            f"  model_has_trend={self.model_has_trend},\n"
            f"  histval={self.histval},\n"
            f"  homotopy_setup={self.homotopy_setup},\n"
            f"  initval_endogenous={self.initval_endogenous},\n"
            f"  initval_exogenous={self.initval_exogenous},\n"
            f"  initval_exogenous_deterministic={self.initval_exogenous_deterministic},\n"
            f"  endval_endogenous={self.endval_endogenous},\n"
            f"  endval_exogenous={self.endval_exogenous},\n"
            f"  endval_exogenous_deterministic={self.endval_exogenous_deterministic},\n"
            f"  scenario={self.scenario},\n"
            f"  shocks={self.shocks},\n"
            f"  perfect_foresight_setup={self.perfect_foresight_setup},\n"
            f"  estimated_parameters={self.estimated_parameters}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_work) -> Self:
        work = Work()
        work.analytical_steadystate_variables = list(
            jl_work.analytical_steadystate_variables
        )
        work.data = jl_work.data
        work.datafile = jl_work.datafile
        work.params = list(jl_work.params)
        work.residuals = list(jl_work.residuals)
        work.dynamic_variables = list(jl_work.dynamic_variables)
        work.exogenous_variables = list(jl_work.exogenous_variables)
        work.observed_variables = list(jl_work.observed_variables)
        work.Sigma_m = jl_work.Sigma_m.to_numpy()
        work.jacobian = jl_work.jacobian.to_numpy()
        work.qr_jacobian = jl_work.qr_jacobian.to_numpy()
        work.model_has_trend = list(jl_work.model_has_trend)
        work.histval = jl_work.histval
        work.homotopy_setup = list(jl_work.homotopy_setup)
        work.initval_endogenous = jl_work.initval_endogenous
        work.initval_exogenous = jl_work.initval_exogenous
        work.initval_exogenous_deterministic = jl_work.initval_exogenous_deterministic
        work.endval_endogenous = jl_work.endval_endogenous
        work.endval_exogenous = jl_work.endval_exogenous
        work.endval_exogenous_deterministic = jl_work.endval_exogenous_deterministic
        work.scenario = jl_work.scenario
        work.shocks = list(jl_work.shocks)
        work.perfect_foresight_setup = jl_work.perfect_foresight_setup
        work.estimated_parameters = EstimatedParameters.from_julia(
            jl_work.estimated_parameters
        )
        return work


@dataclass
class DynareSymbol:
    longname: str
    texname: str
    symboltype: SymbolType
    orderintype: int

    def __repr__(self) -> str:
        return (
            f"DynareSymbol(\n"
            f"  longname={self.longname},\n"
            f"  texname={self.texname},\n"
            f"  symboltype={self.symboltype},\n"
            f"  orderintype={self.orderintype}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_dynaresymbol) -> Self:
        return DynareSymbol(
            longname=jl_dynaresymbol.longname,
            texname=jl_dynaresymbol.texname,
            symboltype=SymbolType.from_julia(jl_dynaresymbol.symboltype),
            orderintype=jl_dynaresymbol.orderintype,
        )


SymbolTable = Dict[str, DynareSymbol]


def symboltable_from_julia(jl_symboltable) -> SymbolTable:
    symboltable = {}
    for key, value in jl_symboltable.items():
        symboltable[key] = DynareSymbol.from_julia(value)
    return symboltable


@dataclass
class Context:
    symboltable: SymbolTable
    models: List[Model]
    modfileinfo: ModFileInfo
    results: Results
    work: Work
    workspaces: Dict[str, Any]

    def __repr__(self) -> str:
        return (
            f"Context(\n"
            f"  symboltable={self.symboltable},\n"
            f"  models={self.models},\n"
            f"  modfileinfo={self.modfileinfo},\n"
            f"  results={self.results},\n"
            f"  work={self.work},\n"
            f"  workspaces={self.workspaces}\n"
            f")"
        )

    @classmethod
    def from_julia(cls, jl_context) -> Self:
        context_py = Context(
            symboltable=symboltable_from_julia(jl_context.symboltable),
            models=[Model.from_julia(jlm) for jlm in jl_context.models],
            modfileinfo=ModFileInfo.from_julia(jl_context.modfileinfo),
            results=Results.from_julia(jl_context.results),
            work=Work.from_julia(jl_context.work),
            workspaces=None,
            # workspaces=from_julia(jl_context.workspaces),
        )
        return context_py
