"""OpenAPI から Tavern 用テストテンプレートを生成するユーティリティ."""

# このモジュールでは OpenAPI ドキュメントとシナリオ定義を読み込み、
# Jinja2 テンプレートを使って Tavern のテスト YAML を作成します。
# 初心者にも読みやすいよう、各処理にコメントを添えています。

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml
from jinja2 import Environment, FileSystemLoader


@dataclass
class Operation:
    """テンプレート描画で使用する API 操作の情報を保持するデータクラス."""

    # OpenAPI から取得した内容を扱いやすい形でまとめています。

    operation_id: str
    custom_name: str
    method: str
    path: str
    request_body: Any
    response_body: Any


def load_yaml(path: str) -> Dict[str, Any]:
    """指定した YAML ファイルを読み込み辞書として返します."""

    file_path = Path(path)
    # ファイルが存在するか確認
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    # YAML を読み込んで Python のデータ構造に変換
    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_example(section: Dict[str, Any]) -> Any:
    """リクエスト/レスポンス定義から example を取得します."""

    content = section.get("content", {})
    media = content.get("application/json", {})
    if isinstance(media, dict):
        return media.get("example", {})
    return {}


def _build_operation_map(openapi: Dict[str, Any]) -> Dict[str, tuple[str, str, Dict[str, Any]]]:
    """operationId からメソッド・パス・詳細を引ける辞書を作成します."""

    operations: Dict[str, tuple[str, str, Dict[str, Any]]] = {}
    # OpenAPI の paths を走査して操作を収集
    for path, methods in openapi.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, op in methods.items():
            if not isinstance(op, dict):
                continue
            op_id = op.get("operationId")
            if op_id:
                operations[op_id] = (method, path, op)
    return operations


def extract_operations(openapi: Dict[str, Any], scenario_items: Iterable[Dict[str, Any]]) -> List[Operation]:
    """シナリオで指定された operationId の情報を抽出します."""

    # OpenAPI 定義から operationId をキーとした辞書を準備
    op_map = _build_operation_map(openapi)
    results: List[Operation] = []

    for item in scenario_items:
        op_id = item.get("operationId")
        if not op_id:
            continue
        # シナリオ上で指定された名称。無ければ operationId をそのまま使う
        custom_name = item.get("name", op_id)

        mapping = op_map.get(op_id)
        if not mapping:
            # 指定された operationId が見つからない場合は警告のみ表示
            print(f"⚠ operationId '{op_id}' がOpenAPI定義に見つかりません。")
            continue
        method, path, op = mapping

        request_body = _get_example(op.get("requestBody", {}))
        response_body = _get_example(op.get("responses", {}).get("200", {}))

        # 取得した情報から Operation インスタンスを作成
        results.append(
            Operation(
                operation_id=op_id,
                custom_name=custom_name,
                method=method,
                path=path,
                request_body=request_body,
                response_body=response_body,
            )
        )

    return results


def generate(
    openapi_file: str, scenario_file: str, template_file: str, output_file: str
) -> None:
    """OpenAPI とシナリオ定義から Tavern 用テストファイルを生成します."""

    for path in [openapi_file, scenario_file, template_file]:
        # 必要なファイルが存在するか確認
        if not Path(path).is_file():
            raise FileNotFoundError(f"Required file not found: {path}")

    openapi = load_yaml(openapi_file)
    scenario = load_yaml(scenario_file)

    test_name = scenario.get("test_name", "テスト")
    scenario_items = scenario.get("scenario", [])

    # シナリオに登場する操作のみを抽出
    operations = extract_operations(openapi, scenario_items)

    template_path = Path(template_file)
    # Jinja2 のテンプレート環境を構築
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["to_nice_yaml"] = lambda value, indent=2: yaml.dump(
        value, allow_unicode=True, default_flow_style=False, indent=indent
    ).rstrip()

    template = env.get_template(template_path.name)
    # テンプレートに値を流し込みテスト YAML を生成
    test_yaml = template.render(test_name=test_name, operations=operations)

    output_path = Path(output_file)
    # 出力先ディレクトリが無ければ作成
    if output_path.parent:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(test_yaml, encoding="utf-8")

    # 生成結果を表示
    print(f"✅ Tavernシナリオテスト生成完了 → {output_file}")


if __name__ == "__main__":
    generate(
        openapi_file="openapi.yaml",
        scenario_file="scenario.yaml",
        template_file="template_scenario.j2",
        output_file="output/test_scenario.tavern.yaml",
    )
