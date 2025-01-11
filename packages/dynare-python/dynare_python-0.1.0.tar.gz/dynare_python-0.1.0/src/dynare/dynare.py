import logging
from pathlib import Path
from juliacall import Main as jl, JuliaError
from .dynare_context import Context
from .errors import DynareError


logger = logging.getLogger("dynare.dynare")


def dynare(model: str | Path) -> Context:
    try:
        if isinstance(model, str):
            model = Path(model)
        jl.seval("using Serialization")
        jl.seval("using Dynare")
        # Double-escape '\' as julia will also interpret the string. Only relevant on Windows
        resolved_path = str(model.resolve()).replace("\\", "\\\\")

        jl.seval(
            "using DataFrames, Tables, PythonCall, Dynare, LinearRationalExpectations"
        )

        # Convert the Julia AxisArrayTable fields of a Context to a Pandas DataFrame with PythonCall.pytable
        jl.seval(
            """
        using Dynare: EstimationResults, EstimatedParameters, SymbolTable, ModFileInfo
                
        struct PyWork
            analytical_steadystate_variables::Vector{Int}
            data::Py
            datafile::String
            params::Vector{Float64}
            residuals::Vector{Float64}
            dynamic_variables::Vector{Float64}
            exogenous_variables::Vector{Float64}
            observed_variables::Vector{String}
            Sigma_m::Matrix{Float64}
            jacobian::Matrix{Float64}
            qr_jacobian::Matrix{Float64}
            model_has_trend::Vector{Bool}
            histval::Matrix{Union{Float64,Missing}}
            homotopy_setup::Vector{NamedTuple{(:name, :type, :index, :endvalue, :startvalue), Tuple{Symbol, SymbolType, Int64, Float64, Union{Float64, Missing}}}}
            initval_endogenous::Matrix{Union{Float64,Missing}}
            initval_exogenous::Matrix{Union{Float64,Missing}}
            initval_exogenous_deterministic::Matrix{Union{Float64,Missing}}
            endval_endogenous::Matrix{Union{Float64,Missing}}
            endval_exogenous::Matrix{Union{Float64,Missing}}
            endval_exogenous_deterministic::Matrix{Union{Float64,Missing}}
            scenario::Dict{PeriodsSinceEpoch, Dict{PeriodsSinceEpoch, Dict{Symbol, Pair{Float64, Symbol}}}}
            shocks::Vector{Float64}
            perfect_foresight_setup::Dict{String,Any}
            estimated_parameters::EstimatedParameters
        end
                
        function convert_to_pywork(work::Work)::PyWork
            # Convert the AxisArrayTable data to a Pandas DataFrame using pytable
            py_data = pytable(work.data)
            
            return PyWork(
                work.analytical_steadystate_variables,
                py_data,
                work.datafile,
                work.params,
                work.residuals,
                work.dynamic_variables,
                work.exogenous_variables,
                work.observed_variables,
                work.Sigma_m,
                work.jacobian,
                work.qr_jacobian,
                work.model_has_trend,
                work.histval,
                work.homotopy_setup,
                work.initval_endogenous,
                work.initval_exogenous,
                work.initval_exogenous_deterministic,
                work.endval_endogenous,
                work.endval_exogenous,
                work.endval_exogenous_deterministic,
                work.scenario,
                work.shocks,
                work.perfect_foresight_setup,
                work.estimated_parameters
            )
        end
                
        struct PySimulation
            firstperiod::PeriodsSinceEpoch
            lastperiod::PeriodsSinceEpoch
            name::String
            statement::String
            data::Py
        end
                
        function convert_to_pysimulation(simulation::Simulation)::PySimulation
            # Convert the AxisArrayTable data to a Pandas DataFrame using pytable
            py_data = pytable(simulation.data)
            
            return PySimulation(
                simulation.firstperiod,
                simulation.lastperiod,
                simulation.name,
                simulation.statement,
                py_data
            )
        end

                
        # Define the PyModelResult structure with Pandas DataFrame fields
        mutable struct PyModelResult
            irfs::Dict{Symbol, Py}
            trends::Trends
            stationary_variables::Vector{Bool}
            estimation::EstimationResults
            filter::Py  # Pandas DataFrame
            forecast::Vector{Py}  # Vector of Pandas DataFrames
            initial_smoother::Py  # Pandas DataFrame
            linearrationalexpectations::LinearRationalExpectationsResults
            simulations::Vector{PySimulation}
            smoother::Py  # Pandas DataFrame
            solution_derivatives::Vector{Matrix{Float64}}
            # sparsegrids::SparsegridsResults
        end

        function convert_to_pymodelresult(model_result::ModelResults)::PyModelResult
            py_irfs = Dict{Symbol, Py}()
            for (key, axis_array_table) in model_result.irfs
                py_irfs[key] = pytable(axis_array_table)
            end

            py_forecast = [pytable(forecast) for forecast in model_result.forecast]
            
            return PyModelResult(
                py_irfs,
                model_result.trends,
                model_result.stationary_variables,
                model_result.estimation,
                pytable(model_result.filter),
                py_forecast,
                pytable(model_result.initial_smoother),
                model_result.linearrationalexpectations,
                [convert_to_pysimulation(simulation) for simulation in model_result.simulations],
                pytable(model_result.smoother),
                model_result.solution_derivatives,
                # model_result.sparsegrids
            )
        end

        struct PyResults
            model_results::Vector{PyModelResult}
        end
                
        struct PyContext
            symboltable::SymbolTable
            models::Vector{Model}
            modfileinfo::ModFileInfo
            results::PyResults  # Now holds PyModelResult instead of ModelResult
            work::PyWork
            workspaces::Dict
        end

        function convert_to_pycontext(ctx::Context)::PyContext
            # Convert each ModelResults in the Context to PyModelResult
            py_model_results = [convert_to_pymodelresult(model_result) for model_result in ctx.results.model_results]

            # Create a PyResults structure with the converted PyModelResults
            py_results = PyResults(py_model_results)

            # Convert the Work structure
            py_work = convert_to_pywork(ctx.work)

            # Return a new PyContext with PyResults and PyWork
            return PyContext(
                ctx.symboltable, 
                ctx.models, 
                ctx.modfileinfo, 
                py_results,  # PyResults instead of Results
                py_work, 
                ctx.workspaces
            )
        end
        """
        )
        context = jl.seval(
            f"""ctx = @dynare "{resolved_path}";
            if !(ctx isa Dynare.Context)
                throw(error("Failed to produce a Dynare context."))
            else
                convert_to_pycontext(ctx)
            end
            """
        )
        return Context.from_julia(context)
    except JuliaError as e:
        raise DynareError.from_julia_error(e)
    except Exception as e:
        raise DynareError(f"An unexpected error occurred: {e}") from e
