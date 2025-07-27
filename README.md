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
[click](https://pypi.org/project/click/):

```bash
pytavoas generate path/to/openapi.yaml --output-dir tests
pytavoas endpoints path/to/openapi.yaml --excel endpoints.xlsx
```

`generate` creates Tavern YAML templates, while `endpoints` lists the
available endpoints and can optionally write them to an Excel file.

