"""Utilities for listing OpenAPI endpoints."""

from __future__ import annotations

from pathlib import Path
import os
import yaml
import openpyxl
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet
from typing import Any


def load_openapi_yaml(file_path: str) -> dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_operations(openapi: dict[str, Any]) -> list[dict[str, str]]:
    operations: list[dict[str, str]] = []
    paths = openapi.get("paths", {})
    for path, methods in paths.items():
        if methods is None:
            continue
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            operation_id = details.get("operationId") or ""
            summary = details.get("summary") or ""
            operations.append(
                {
                    "operationId": operation_id,
                    "summary": summary,
                    "method": method.upper(),
                    "url": path,
                }
            )
    return operations


def write_to_excel(operations: list[dict[str, str]], output_path: str) -> None:

    wb = openpyxl.Workbook()
    ws: Worksheet = wb.active  # type: ignore # 型を明示して Pylance 警告を防ぐ
    ws.title = "OpenAPI Operations"

    headers = ["operationId", "summary", "method", "url"]
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)

    for op in operations:
        ws.append([op["operationId"], op["summary"], op["method"], op["url"]])

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    wb.save(output_path)


def list_endpoints(input_file: str, output_file: str) -> None:
    """List endpoints and optionally write them to an Excel file."""
    openapi = load_openapi_yaml(input_file)
    operations = extract_operations(openapi)
    write_to_excel(operations, output_file)
    print(f"✅ エクセルファイルに出力完了: {output_file}")


if __name__ == "__main__":
    list_endpoints(
        input_file="openapi.yaml", output_file="output/openapi_operations.xlsx"
    )
