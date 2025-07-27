"""Utilities for generating Tavern test templates from OpenAPI definitions."""

from __future__ import annotations

from pathlib import Path
import yaml
import os
import sys
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Any


def load_yaml(path: str) -> dict:
    if not os.path.isfile(path):
        print(f"❌ ファイルが見つかりません: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_operations(openapi: dict, scenario_items: List[dict]) -> List[dict]:
    paths = openapi.get("paths", {})
    results = []

    for item in scenario_items:
        op_id = item.get("operationId")
        custom_name = item.get("name", op_id)
        found = False

        for path, methods in paths.items():
            for method, op in methods.items():
                if not isinstance(op, dict):
                    continue
                if op.get("operationId") == op_id:
                    found = True

                    request_body = {}
                    if "requestBody" in op:
                        content = op["requestBody"].get("content", {})
                        app_json = content.get("application/json", {})
                        if isinstance(app_json, dict):
                            example = app_json.get("example")
                            if example:
                                request_body = example

                    response_body = {}
                    responses = op.get("responses", {})
                    if "200" in responses:
                        content = responses["200"].get("content", {})
                        app_json = content.get("application/json", {})
                        if isinstance(app_json, dict):
                            example = app_json.get("example")
                            if example:
                                response_body = example

                    results.append(
                        {
                            "operation_id": op_id,
                            "custom_name": custom_name,
                            "method": method,
                            "path": path,
                            "request_body": request_body,
                            "response_body": response_body,
                        }
                    )

        if not found:
            print(f"⚠ operationId '{op_id}' がOpenAPI定義に見つかりません。")

    return results


def generate(
    openapi_file: str, scenario_file: str, template_file: str, output_file: str
) -> None:
    for f in [openapi_file, scenario_file, template_file]:
        if not os.path.isfile(f):
            print(f"❌ 必要なファイルが見つかりません: {f}")
            sys.exit(1)

    openapi = load_yaml(openapi_file)
    scenario = load_yaml(scenario_file)

    test_name = scenario.get("test_name", "テスト")
    scenario_items = scenario.get("scenario", [])

    operations = extract_operations(openapi, scenario_items)

    template_dir = os.path.dirname(template_file)
    template_name = os.path.basename(template_file)
    env = Environment(
        loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
    )
    env.filters["to_nice_yaml"] = lambda value, indent=2: yaml.dump(
        value, allow_unicode=True, default_flow_style=False, indent=indent
    ).rstrip()

    template = env.get_template(template_name)
    test_yaml = template.render(test_name=test_name, operations=operations)

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(test_yaml)

    print(f"✅ Tavernシナリオテスト生成完了 → {output_file}")


if __name__ == "__main__":
    generate(
        openapi_file="openapi.yaml",
        scenario_file="scenario.yaml",
        template_file="template_scenario.j2",
        output_file="output/test_scenario.tavern.yaml",
    )
