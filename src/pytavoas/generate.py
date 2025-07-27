"""Utilities for generating Tavern test templates from OpenAPI definitions."""

from __future__ import annotations

from pathlib import Path


def generate(openapi_file: str, output_dir: str) -> None:
    """Generate Tavern YAML templates from OPENAPI_FILE."""
    input_path = Path(openapi_file)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # TODO: Parse the OpenAPI file and generate Tavern templates.
    # For now just create a placeholder file.
    placeholder = out_dir / "placeholder.tavern.yaml"
    placeholder.write_text(
        f"# Tavern test templates generated from {input_path.name}\n"
    )

