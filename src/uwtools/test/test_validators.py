"""
Tests for schema validation tool
"""

import io
import json
import os
import pathlib
from contextlib import redirect_stdout

import jsonschema
import pytest
import yaml

uwtools_file_base = os.path.join(os.path.dirname(__file__))


@pytest.mark.skip()
def test_validate_yaml_salad():
    """
    Test that simple salad schema is accepted as valid json schema and that it
    validates both valid and bad input files
    """
    schema_fn = os.path.join(
        os.path.dirname(uwtools_file_base), pathlib.Path("schema/salad.jsonschema")
    )
    input_fn = os.path.join(uwtools_file_base, pathlib.Path("fixtures/fruit_config_similar.yaml"))
    bad_input_fn = os.path.join(uwtools_file_base, pathlib.Path("fixtures/bad_fruit_config.yaml"))

    with open(schema_fn, "r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
        with open(input_fn, encoding="utf-8") as input_file:
            infile = yaml.safe_load(input_file)
        outstring = io.StringIO()
        with redirect_stdout(outstring):
            jsonschema.validate(infile, schema)
        result = outstring.getvalue()
        assert result == ""

        with open(bad_input_fn, encoding="utf-8") as bad_input_file:
            bad_infile = yaml.safe_load(bad_input_file)
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(bad_infile, schema)
