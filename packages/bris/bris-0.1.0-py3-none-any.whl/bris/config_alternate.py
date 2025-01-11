import bris.output
from bris import utils


def get_routes(routing_config: dict, data_module: DataModule, run_name: str, workdir: str):
    """
    Args:
        routing_config: Dictionary from config file
        data_module: Data module
        run_name: Name of this run used by outputs to set filenames
    Returns:
        dict:
            key (tuple): (decoder_index, start_gridpoint, end_gridpoint)
            value (list): List of outputs
    """
    ret = dict()
    for name, config in routing_config.items():
        key = (decoder_index, start_gridpoint, end_gridpoint)
        outputs = list()
        for output_type, output_config in config["outputs"].items():
            args = output_config
            if "filename" in args:
                args["filename"] = expand_run_name(args["filename"], run_name)
            curr_workdir = utils.get_workdir(workdir)

            if output_type == "verif":
                for variable in args["variables"]:
                    curr_args = {k,v for k,v in args.items() if k not in ["variables"]}
                    curr_args["variable"] = variable
                    curr_args["filename"] = expand_variable(curr_args["filename"], variable)
                    output = bris.output.instantiate(output_type, predict_metadata, curr_workdir,
                            curr_args)
            else:
                output = bris.output.instantiate(output_type, predict_metadata, curr_workdir, args)
        ret[key] = outputs

    return ret

def expand_run_name(string, run_name):
    return string.replace("%R", run_name)

def expand_variable(string, variable):
    return string.replace("%V", variable)
