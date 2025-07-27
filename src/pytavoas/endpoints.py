"""Utilities for listing OpenAPI endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List

import openpyxl
import yaml
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class Endpoint:
    """Simplified representation of an API operation."""

    operation_id: str
    summary: str
    method: str
    url: str


def load_openapi_yaml(file_path: str) -> dict[str, Any]:
    """Load an OpenAPI document from *file_path*."""

    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def extract_operations(openapi: dict[str, Any]) -> List[Endpoint]:
    """Return a list of :class:`Endpoint` objects from *openapi* definition."""

    results: List[Endpoint] = []
    for path, methods in openapi.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            operation_id = str(details.get("operationId", ""))
            summary = str(details.get("summary", ""))
            results.append(
                Endpoint(
                    operation_id=operation_id,
                    summary=summary,
                    method=method.upper(),
                    url=path,
                )
            )
    return results


def write_to_excel(operations: Iterable[Endpoint], output_path: str) -> None:
    """Write *operations* information to an Excel spreadsheet."""

    wb = openpyxl.Workbook()
    ws: Worksheet = wb.active  # type: ignore[assignment]
    ws.title = "OpenAPI Operations"

    headers = ["operationId", "summary", "method", "url"]
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)

    for op in operations:
        ws.append([op.operation_id, op.summary, op.method, op.url])

    output_path_p = Path(output_path)
    if output_path_p.parent:
        output_path_p.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path_p))


def list_endpoints(input_file: str, output_file: str) -> None:
    """List endpoints defined in *input_file* and save them to *output_file*."""

    openapi = load_openapi_yaml(input_file)
    operations = extract_operations(openapi)
    write_to_excel(operations, output_file)
    print(f"✅ エクセルファイルに出力完了: {output_file}")


if __name__ == "__main__":
    list_endpoints(
        input_file="openapi.yaml", output_file="output/openapi_operations.xlsx"
    )
