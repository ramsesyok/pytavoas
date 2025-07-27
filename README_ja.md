# pytavoas 日本語版

`pytavoas` は [OpenAPI](https://www.openapis.org/) 定義をもとに [Tavern](https://taverntesting.github.io/) 用のテストテンプレートを生成し、必要に応じてエンドポイント一覧を Excel 形式で出力する CLI ツールです。

## インストール

Python 3.11 以上の環境でソースからインストールします。

```bash
pip install -e .
```

## 使い方

`pytavoas` にはふたつのサブコマンドがあります。各オプションは必須です。

- `generate`  : OpenAPI とシナリオ、Jinja2 テンプレートから Tavern テストファイルを生成します。
- `endpoints` : OpenAPI に登録されている操作一覧を Excel ファイルとして保存します。

### テストテンプレートの生成

以下のコマンドは `openapi.yaml` とシナリオ `scenario.yaml`、テンプレート `template_scenario.j2` からテストファイルを生成し、`output/test_scenario.tavern.yaml` に保存します。

```bash
pytavoas generate openapi.yaml \
    --scenario scenario.yaml \
    --template template_scenario.j2 \
    --output output/test_scenario.tavern.yaml
```

シナリオファイルは次のような YAML で、テスト名と実行したい `operationId` を順番に記述します。

```yaml
test_name: "シナリオテスト1"
scenario:
  - name: ペットの追加
    operationId: addPet
  - name: ペット情報の更新
    operationId: updatePet
```

### エンドポイント一覧の出力

OpenAPI ファイルの全エンドポイントを一覧にして Excel へ保存するには次のように実行します。

```bash
pytavoas endpoints openapi.yaml --output output/openapi_operations.xlsx
```

## テンプレートについて

付属の `template_scenario.j2` は生成される Tavern テストの雛形です。`stages` ごとにリクエスト情報と期待レスポンスを記述する一般的な構成になっています。

必要に応じてこのテンプレートを編集することで、ヘッダーや認証など独自の設定を加えることができます。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。
