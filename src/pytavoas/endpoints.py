"""OpenAPI のエンドポイントを一覧化するためのユーティリティ."""

# Excel への書き出しや YAML の読み込みなど、主に補助的な処理を
# まとめたモジュールです。コードの流れが追いやすいように
# 関数ごとに簡単な説明を付けています。

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
    """API の各操作をシンプルに表現したデータクラス."""

    # Excel への出力などで扱いやすい形にフィールドをまとめています。

    operation_id: str
    summary: str
    method: str
    url: str


def load_openapi_yaml(file_path: str) -> dict[str, Any]:
    """OpenAPI ファイルを読み込んで辞書として返します."""

    path = Path(file_path)
    # 指定されたファイルが存在しなければエラーにします
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    # YAML を読み込み空の場合は空の辞書を返します
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def extract_operations(openapi: dict[str, Any]) -> List[Endpoint]:
    """OpenAPI 定義から :class:`Endpoint` のリストを作成します."""

    results: List[Endpoint] = []
    # paths 以下を走査して各 HTTP メソッドの情報を取り出します
    for path, methods in openapi.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, details in methods.items():
            if not isinstance(details, dict):
                continue
            # operationId や summary が無い場合は空文字列として扱います
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
    """操作一覧を Excel ファイルへ書き出します."""

    # 新しいワークブック(Excel ファイル)を作成

    wb = openpyxl.Workbook()
    # 先頭のワークシートを取得し表題を設定
    ws: Worksheet = wb.active  # type: ignore[assignment]
    ws.title = "OpenAPI Operations"

    headers = ["operationId", "summary", "method", "url"]
    # 1 行目にヘッダーを書き込む
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        # ヘッダーを太字にする
        cell.font = Font(bold=True)

    for op in operations:
        # Endpoint オブジェクトの各フィールドを1行にして追加
        ws.append([op.operation_id, op.summary, op.method, op.url])

    output_path_p = Path(output_path)
    # 出力先ディレクトリが無ければ作成
    if output_path_p.parent:
        output_path_p.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path_p))


def list_endpoints(input_file: str, output_file: str) -> None:
    """OpenAPI ファイルのエンドポイントを取得し Excel へ保存します."""

    # OpenAPI を読み込んで操作情報を抽出

    openapi = load_openapi_yaml(input_file)
    operations = extract_operations(openapi)
    # 取得した操作を Excel ファイルに書き出す
    write_to_excel(operations, output_file)
    print(f"✅ エクセルファイルに出力完了: {output_file}")


if __name__ == "__main__":
    list_endpoints(
        input_file="openapi.yaml", output_file="output/openapi_operations.xlsx"
    )
