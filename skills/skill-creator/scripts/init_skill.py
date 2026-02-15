#!/usr/bin/env python3
"""
スキルの雛形ディレクトリを生成する。

Usage:
    python init_skill.py <skill-name> --path <output-directory>

Example:
    python init_skill.py my-analyzer --path skills/
    python init_skill.py report-builder --path /tmp/skills
"""

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# テンプレート
# ---------------------------------------------------------------------------

SKILL_MD = """\
---
name: {name}
description: "TODO: このスキルが何をするか、どんな場面で使うかを書く。description はスキルの発動条件を決める最重要テキスト。"
---

# {title}

## 概要

TODO: スキルの目的を1-2文で説明する。

## 手順

TODO: スキルの構成に合った見出し構造を選ぶ。

- ワークフロー型: Step 1 → Step 2 → ...
- タスク型: 操作A / 操作B / ...
- リファレンス型: ガイドライン / 仕様 / ...

不要なリソースディレクトリ（scripts/, references/, assets/）は削除して構わない。
"""

SAMPLE_SCRIPT = """\
#!/usr/bin/env python3
\"\"\"
{name} 用のサンプルスクリプト。

実際の処理に置き換えるか、不要なら削除する。
\"\"\"

import sys


def run():
    print(f"[{name}] サンプルスクリプトが実行されました。")


if __name__ == "__main__":
    run()
"""

SAMPLE_REFERENCE = """\
# {title} リファレンス

TODO: スキルの作業中に参照するドキュメントをここに置く。

- API仕様、スキーマ定義、品質チェックリストなど
- SKILL.md から参照パスと読み込みタイミングを明記すること

不要なら削除する。
"""

SAMPLE_ASSET = """\
このディレクトリには出力生成時に使うファイルを置く。
テンプレート、画像、フォントなど。

不要なら削除する。
"""


def to_title(name: str) -> str:
    """ハイフン区切りの名前をタイトルケースに変換する。"""
    return " ".join(w.capitalize() for w in name.split("-"))


def create_skill(name: str, base_path: str) -> Path:
    target = Path(base_path).resolve() / name

    if target.exists():
        print(f"[error] ディレクトリが既に存在します: {target}", file=sys.stderr)
        sys.exit(1)

    title = to_title(name)

    # ディレクトリ作成
    target.mkdir(parents=True)
    (target / "scripts").mkdir()
    (target / "references").mkdir()
    (target / "assets").mkdir()

    # SKILL.md
    (target / "SKILL.md").write_text(SKILL_MD.format(name=name, title=title))

    # サンプルファイル
    script_path = target / "scripts" / "sample.py"
    script_path.write_text(SAMPLE_SCRIPT.format(name=name))
    script_path.chmod(0o755)

    (target / "references" / "reference.md").write_text(
        SAMPLE_REFERENCE.format(title=title)
    )
    (target / "assets" / "README.txt").write_text(SAMPLE_ASSET)

    return target


def main():
    parser = argparse.ArgumentParser(
        description="スキルの雛形ディレクトリを生成する。"
    )
    parser.add_argument("name", help="スキル名（ハイフン区切り小文字）")
    parser.add_argument("--path", required=True, help="出力先の親ディレクトリ")
    args = parser.parse_args()

    target = create_skill(args.name, args.path)

    print(f"スキルを作成しました: {target}")
    print()
    print("次のステップ:")
    print("  1. SKILL.md の TODO を埋める")
    print("  2. scripts/, references/, assets/ を必要に応じて編集・削除する")


if __name__ == "__main__":
    main()
