"""pytavoas のコマンドラインインターフェース."""

# このモジュールでは [click](https://click.palletsprojects.com/) を用いて
# シンプルな CLI を定義しています。"pytavoas" コマンドを実行すると
# ここに定義したサブコマンドが利用できます。

import click

from . import generate, endpoints


@click.group()
def cli():
    """コマンドのグループを定義するエントリーポイント."""
    # `pytavoas` の後に続くサブコマンドをまとめるための関数です。


@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.argument("scenario_file", type=click.Path(exists=True))
@click.argument("template_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def generate_cmd(
    openapi_file: str, scenario_file: str, template_file: str, output_file: str
) -> None:
    """OpenAPI から Tavern テストを生成するサブコマンド."""
    # 実際の処理は ``generate.generate`` 関数に委譲しています。
    generate.generate(
        openapi_file=openapi_file,
        scenario_file=scenario_file,
        template_file=template_file,
        output_file=output_file,
    )


@cli.command()
@click.argument("openapi_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def endpoints_cmd(openapi_file: str, output_file: str) -> None:
    """OpenAPI に定義されたエンドポイント一覧を出力するサブコマンド."""
    # Excel への書き出しなどの処理は ``endpoints.list_endpoints`` が行います。
    endpoints.list_endpoints(input_file=openapi_file, output_file=output_file)


def main() -> None:
    """``pytavoas`` コマンドの実行入口."""
    # `setup.py` や `pyproject.toml` から呼び出される想定です。
    cli()


if __name__ == "__main__":
    main()
