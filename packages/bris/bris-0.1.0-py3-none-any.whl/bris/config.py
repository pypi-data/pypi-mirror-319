import json
import jsonschema
import os
import yaml


def validate(filename, raise_on_error=False):
    schema_filename = os.path.dirname(os.path.abspath(__file__)) + "/schema/schema.json"
    with open(schema_filename) as file:
        schema = json.load(file)

    with open(filename) as file:
        config = yaml.safe_load(file)
    try:
        q = jsonschema.validate(instance=config, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        if raise_on_error:
            raise
        else:
            print("WARNING: Schema does not validate")
            print(e)


if __name__ == "__main__":
    filename = "config.yaml"
    validate(filename)
