"""Utilities for listing OpenAPI endpoints."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def _parse_openapi(file_path: Path) -> Iterable[str]:
    """Parse OpenAPI file and yield endpoint paths.

    This is a simplified placeholder implementation.
    """
    # TODO: Implement real parser for OpenAPI specification.
    # Here we just return a fixed list for demonstration.
    return ["/users", "/items"]


def list_endpoints(openapi_file: str, excel: str | None = None) -> None:
    """List endpoints and optionally write them to an Excel file."""
    file_path = Path(openapi_file)
    endpoints = list(_parse_openapi(file_path))
    for ep in endpoints:
        print(ep)

    if excel:
        try:
            import pandas as pd  # type: ignore
        except Exception as exc:  # pragma: no cover - error path
            raise RuntimeError(
                "pandas is required for writing Excel files"
            ) from exc
        df = pd.DataFrame({"endpoint": endpoints})
        df.to_excel(excel, index=False)

