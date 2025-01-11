from collections import defaultdict

import numpy as np

import bris.outputs
from bris import utils
from bris.data.datamodule import DataModule
from bris.predict_metadata import PredictMetadata


def get(
    routing_config: dict,
    num_leadtimes: int,
    num_members: int,
    data_module: DataModule,
    run_name: str,
    workdir: str,
):
    """Returns outputs for each decoder and domain

    This is used by the CustomWriter

    Args:
        routing_config: Dictionary from config file
        num_leadtimes: Number of leadtimes that the model will produce
        data_module: Data module
        run_name: Name of this run used by outputs to set filenames
    Returns:
        list of dicts:
            decoder_index (int)
            domain_index (int)
            start_gridpoint (int)
            end_gridpoint (int)
            outputs (list)
        dicts:
            decoder_index -> variable_indices

    """
    ret = list()
    required_variables = get_required_variables(routing_config, data_module)

    for config in routing_config:
        decoder_index = config["decoder_index"]
        domain_index = config["domain"]

        curr_grids = data_module.grids[decoder_index]
        if domain_index == 0:
            start_gridpoint = 0
            end_gridpoint = curr_grids[domain_index]
        else:
            start_gridpoint = np.sum(curr_grids[0:domain_index])
            end_gridpoint = start_gridpoint + curr_grids[domain_index]

        outputs = list()
        for oc in config["outputs"]:
            # TODO: Get this from data_module
            variables = ["u_800", "u_600", "2t", "v_500", "10u"]
            lats = data_module.latitudes[decoder_index][start_gridpoint:end_gridpoint]
            lons = data_module.longitudes[decoder_index][start_gridpoint:end_gridpoint]
            field_shape = data_module.field_shape[decoder_index][domain_index]

            curr_required_variables = required_variables[decoder_index]

            pm = PredictMetadata(
                curr_required_variables,
                lats,
                lons,
                num_leadtimes,
                num_members,
                field_shape,
            )

            for output_type, args in oc.items():
                if "filename" in args:
                    args["filename"] = expand_run_name(args["filename"], run_name)

                curr_workdir = utils.get_workdir(workdir)
                output = bris.outputs.instantiate(output_type, pm, curr_workdir, args)
                outputs += [output]

        variable_indices = dict()
        for decoder_index, r in required_variables.items():
            variable_indices[decoder_index] = list()
            for name in required_variables[decoder_index]:
                index = data_module.name_to_index[decoder_index][name]
                variable_indices[decoder_index] += [index]

        # We don't need to pass out domain_index, since this is only used to get start/end
        # gridpoints and is not used elsewhere in the code
        ret += [
            dict(
                decoder_index=decoder_index,
                start_gridpoint=start_gridpoint,
                end_gridpoint=end_gridpoint,
                outputs=outputs,
            )
        ]

    return ret


def get_variable_indices(routing_config: dict, data_module: DataModule):
    """Returns a list of variable indices for each decoder

    This is used by Model
    """
    required_variables = get_required_variables(routing_config, data_module)

    variable_indices = dict()
    for decoder_index, r in required_variables.items():
        variable_indices[decoder_index] = list()
        for name in required_variables[decoder_index]:
            index = data_module.name_to_index[decoder_index][name]
            variable_indices[decoder_index] += [index]

    return variable_indices


def get_required_variables(routing_config: dict, data_module: DataModule):
    """Returns a list of required variables for each decoder"""
    required_variables = defaultdict(list)
    for rc in routing_config:
        l = list()
        for oc in rc["outputs"]:
            for output_type, args in oc.items():
                l += bris.outputs.get_required_variables(output_type, args)
        required_variables[rc["decoder_index"]] += l

    for decoder_index, v in required_variables.items():
        if None in v:
            name_to_index = data_module.name_to_index[decoder_index]

            # Pre-initialize list
            required_variables[decoder_index] = list(name_to_index.keys())

            for name, index in name_to_index.items():
                assert index < len(name_to_index)

                required_variables[decoder_index][index] = name
        else:
            required_variables[decoder_index] = sorted(list(set(v)))

    return required_variables


def expand_run_name(string, run_name):
    return string.replace("%R", run_name)


def expand_variable(string, variable):
    return string.replace("%V", variable)
