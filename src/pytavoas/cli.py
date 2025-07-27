"""Command line interface for pytavoas."""

import click

from . import generate, endpoints


@click.group()
def cli():
    """pytavoas command line."""


@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.argument("scenario_file", type=click.Path(exists=True))
@click.argument("template_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(exists=True))
def generate_cmd(
    openapi_file: str, scenario_file: str, template_file: str, output_file: str
) -> None:
    """Generate Tavern test templates from OPENAPI_FILE."""
    generate.generate(
        openapi_file=openapi_file,
        scenario_file="scenario.yaml",
        template_file="template_scenario.j2",
        output_file="output/test_scenario.tavern.yaml",
    )


@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(exists=True))
def endpoints_cmd(openapi_file: str, output_file: str) -> None:
    """List endpoints defined in OPENAPI_FILE."""
    endpoints.list_endpoints(input_file=openapi_file, output_file=output_file)


def main() -> None:
    """Entry point for console_scripts."""
    cli()


if __name__ == "__main__":
    main()
