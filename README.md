# pytavoas

A CLI tool to generate [Tavern](https://taverntesting.github.io/) test
templates from OpenAPI definitions and optionally output a list of
endpoints to an Excel file.

## Installation

Install from source in an environment with Python 3.11 or higher:

```bash
pip install -e .
```

## Usage

The command line tool provides two subcommands using
[click](https://pypi.org/project/click/). Each option is required:

```bash
# Generate Tavern test templates using a scenario and Jinja template
pytavoas generate openapi.yaml \
    --scenario scenario.yaml \
    --template template_scenario.j2 \
    --output output/test_scenario.tavern.yaml

# List all endpoints to an Excel file
pytavoas endpoints openapi.yaml --output output/openapi_operations.xlsx
```

`generate` reads an OpenAPI document, scenario YAML and Jinja2 template and
writes a Tavern test file. `endpoints` lists the available operations and can
output them to an Excel spreadsheet.

