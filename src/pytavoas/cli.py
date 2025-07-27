"""Command line interface for pytavoas."""

import click

from . import generate, endpoints

@click.group()
def cli():
    """pytavoas command line."""

@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    default="tests",
    help="Directory to write Tavern test templates.",
    show_default=True,
)
def generate_cmd(openapi_file: str, output_dir: str) -> None:
    """Generate Tavern test templates from OPENAPI_FILE."""
    generate.generate(openapi_file, output_dir)


@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.option(
    "--excel",
    type=click.Path(),
    help="Write endpoints summary to an Excel file if provided.",
)
def endpoints_cmd(openapi_file: str, excel: str | None) -> None:
    """List endpoints defined in OPENAPI_FILE."""
    endpoints.list_endpoints(openapi_file, excel)


def main() -> None:
    """Entry point for console_scripts."""
    cli()


if __name__ == "__main__":
    main()
